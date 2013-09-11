""" Curriculum-based course timetabling solver;
    solves timetabling problems formulated in .ectt file format (http://tabu.diegm.uniud.it/ctt/)
    Copyright (C) 2013  Stephan E. Becker

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

__author__ = 'Stephan Becker'
import os
import time

import initialisation


# the time limit in seconds
# max_runtime = initialisation.max_runtime
# timelimit_construction = time.clock() + initialisation.max_construction
# timelimit = time.clock() + max_runtime

starting_time = time.clock()


# penalty weights according to the UD specification by (De Cesco, Di Gaspero, Schaerf, 2012)
# UD2 (= ITC-2) specs: 1-5-2-1
RoomCapacityPenalty = 1
MinWorkingDays = 5
IsolatedLectures = 2
RoomStability = 1


#1 Import the .ectt data to python


test_instances = ["toy.ectt"]
comp_instances = ["toy.ectt"]
for i in range(1, 22):
    new_instance = "comp{:02}.ectt".format(i)
    comp_instances.append(new_instance)
for i in range(1, 5):
    new_instance = "test{}.ectt".format(i)
    test_instances.append(new_instance)

# print(test_instances)
# print(comp_instances)

# input_file_choice = test_instances[0]
# input_file=comp_instances[0]

all_instances = [test_instances, comp_instances]


def promptUserForInstanceChoice():
    """
    asks the user to select an instance, returns input_file
    """
    choice_type = int(input("Select a dataset; press 0 for test or 1 for comp>>>>"))
    choice_number = int(input("Select an instance from the dataset; press 0 for toy, 1-4 for test, 1-21 for comp>>>>"))
    return all_instances[choice_type][choice_number]


input_file_choice = all_instances[initialisation.choice_set][initialisation.choice_inst]


# input_file_choice=promptUserForInstanceChoice()


datasets_dir = os.path.join(os.path.dirname(__file__), 'datasets') + "\\"

input_file = datasets_dir + input_file_choice

ttFile = open(input_file)

InputTTData = []
for line in ttFile:
    line = line[:-1] # last character is a newline
    InputTTData.append(line)

ttFile.close()


def prep_data(section_name):
    """
    prepares the raw data for the algo:
    splits the raw list into sections,
    splits the section string into a list,
    turns number strings into integers
    """
    if section_name == "HEADER":
        start = 0
    else:
        start = InputTTData.index(section_name) + 1 # don't include the section name in the list
    stop = InputTTData.index("", start)
    tmp_section = InputTTData[start:stop]
    section = []
    for i in tmp_section:
        part = i.split()
        part2 = []
        for element in part:
            try:
                e = int(element)
            except:
                e = element
            finally:
                part2.append(e)
        section.append(part2)
    return section


#Header
# Section "HEADER"
header1 = prep_data("HEADER")


class Header:
    def __init__(self, header):
        self.name = header[0][1].lower()
        self.courses = header[1][1]
        self.rooms = header[2][1]
        self.days = header[3][1]
        self.periods = header[4][1]
        self.curricula = header[5][1]
        self.min_daily = header[6][1]
        self.unavailabilities = header[7][1]
        self.room_constraints = header[8][1]
        self.max_daily = header[6][2]

    def __repr__(self):
        return "<Name: {}, courses: {}, rooms: {}, days {}>".format(self.name, self.courses, self.rooms, self.days)


header = Header(header1)



# List of courses
# Section "COURSES:"
# <CourseID> <Teacher> <# Lectures> <MinWorkingDays> <# Students> <Double Lectures>
courses1 = prep_data("COURSES:")


class Course:
    def __init__(self, course):
        self.id = course[0]
        self.teacher = course[1]
        self.num_lectures = course[2]
        self.minWorkingDays = course[3]
        self.num_students = course[4]
        self.double_lectures = course[5]
        self.xx_num_lectures_initial = course[2]

    def decreaseLectures(self):
        if self.num_lectures > 0:
            self.num_lectures -= 1
        else:
            raise Exception("lectures below 0")

    def increaseLectures(self):
        self.num_lectures += 1
        #Debug
        if self.num_lectures > self.xx_num_lectures_initial:
            raise Exception("too many lectures")


    def finished(self):
        return self.num_lectures == 0

    def __repr__(self):
        return "<ID: {}, teacher: {}, lectures: {}, working days: {}, students: {}, doubles: {}>" \
            .format(self.id, self.teacher, self.num_lectures, self.minWorkingDays,
                    self.num_students, self.double_lectures)


courses = [Course(c) for c in courses1]


class Event:
    def __init__(self, course):
        self.id = course[0]
        self.teacher = course[1]
        self.minWorkingDays = course[3]
        self.num_students = course[4]
        self.double_lectures = course[5]

    # def __repr__(self):
    #     return "<ID: {}, teacher: {}, working days: {}, students: {}, doubles: {}>"\
    #         .format(self.id,self.teacher,self.minWorkingDays,
    #                 self.num_students,self.double_lectures)

    def __repr__(self):
        return "<{}>".format(self.id)


events = [Event(c) for c in courses1 for i in range(c[2])]

# print(events)

# List of rooms
# Section "ROOMS:"
# <RoomID> <Capacity> <Site>
rooms1 = prep_data("ROOMS:")


class Room:
    def __init__(self, room):
        self.id = room[0]
        self.capacity = room[1]
        self.site = room[2]

    def __repr__(self):
        return "<ID: {}, cap: {}, site: {}>".format(self.id, self.capacity, self.site)


rooms = [Room(r) for r in rooms1]

# mapping the roomIndex to the roomName
roomIndexToName = {}
for roomIndex, room in enumerate(rooms1):
    roomIndexToName[roomIndex] = room[0]



# List of curricula
# Section "CURRICULA:"
# <CurriculumID> <# Courses> <CourseID> ... <CourseID>
curricula1 = prep_data("CURRICULA:")


class Curriculum:
    def __init__(self, cu):
        self.id = cu[0]
        self.num_courses = cu[1]
        self.courses = cu[2:]

    def __repr__(self):
        return "<ID: {}, num_courses: {}, courses: {}>".format(self.id, self.num_courses, self.courses)


curricula = [Curriculum(c) for c in curricula1]



# List of unavailability_constraints
# Section "UNAVAILABILITY_CONSTRAINTS:"
# <CourseID> <Day> <Day_Period>
# All IDs are strings without blanks starting with a letter. Days and periods start from 0.
# For example, the constraint TecCos 3 2 states that
# course TecCos cannot be scheduled in the third (2) period of Thursdays (3).
unavailability_constraints_org = prep_data("UNAVAILABILITY_CONSTRAINTS:")


class Unavailability:
    def __init__(self, una):
        self.courseID = una[0]
        self.day = una[1]
        self.dayPeriod = una[2]
        self.timeslot = una[1] * header.periods + una[2] # Day*numberOfPeriodsPerDay + Day_Period = timeslot

    def __repr__(self):
        return "<course: {}, timeslot: {}>".format(self.courseID, self.timeslot)


# modified list of unavailability_constraints,
# <CourseID> <Timeslot>
unavailability_constraints1 = []
for constraint in unavailability_constraints_org:
    newlist = []
    newlist.append(constraint[0])
    timeslot = constraint[1] * header.periods + constraint[2]  # Day*numberOfPeriodsPerDay + Day_Period = timeslot
    newlist.append(timeslot)
    unavailability_constraints1.append(newlist)

unavailability_constraints = [Unavailability(u) for u in unavailability_constraints_org]



# List of ROOM_CONSTRAINTS
# Section "ROOM_CONSTRAINTS:"
# <CourseID> <RoomID>
room_constraints1 = prep_data("ROOM_CONSTRAINTS:")


class RoomConstraint:
    def __init__(self, rc):
        self.courseID = rc[0]
        self.roomID = rc[1]

    def __repr__(self):
        return "<course: {}, room: {}>".format(self.courseID, self.roomID)


room_constraints = [RoomConstraint(rc) for rc in room_constraints1]



# numberOfTimeslots == Days * PeriodsPerDay
# numberOfTimeslots = header[3][1] * header[4][1]
numberOfTimeslots = header.days * header.periods
numberOfRooms = len(rooms)


# Timetable == Rooms(rows) * Timeslots(columns)
# tt = numpy.empty((numberOfRooms, numberOfTimeslots))



# mapping a timeslot to a day and dayPeriod
mapTimeslotToDayAndPeriod = {}
for i in range(numberOfTimeslots):
    mapTimeslotToDayAndPeriod[i] = (i // header.periods, i % header.periods)


def convertTimeslotToDayPeriod(timeslot):
    """
    returns the day and dayPeriod of a timeslot
    """
    day, period = mapTimeslotToDayAndPeriod[timeslot]
    return day, period


days = []
day = []
for ts in range(numberOfTimeslots):
    day.append(ts)
    if ts % header.periods == header.periods - 1:
        days.append(day)
        day = []



# global variables

unplacedEvents = []


# List of courses with the same teacher,
# dict mapping a teacher to all his courses
teachers = {}
for course in courses:
    teacher = course.teacher
    if teacher not in teachers:
        teachers[teacher] = []
    teachers[teacher].append(course.id)


# Map the course_name to its index in "courses"
courseNameToIndex = {}
for i, course in enumerate(courses):
    courseNameToIndex[course.id] = i



# mapping of the curriculum to the courses in the curriculum
curriculaToCourses = {}
for cu in curricula:
    curriculaToCourses[cu.id] = cu.courses



# mapping of the course to all curricula containing the course
coursesToCurricula = {}
for course in courses:
    coursesToCurricula[course.id] = []
    for cu, cuList in curriculaToCourses.items():
        if course.id in cuList:
            coursesToCurricula[course.id].append(cu)



# create an empty timetable as a dictionary with (room, timeslot), create a list of empty positions (room, timeslot)
timetable = {}
emptyPositions = [] # hard constraint: RoomOccupancy
for i in range(numberOfRooms):
    for j in range(numberOfTimeslots):
        emptyPositions.append((i, j))
        timetable[(i, j)] = None

forbiddenPositions = []


def getEmptyPositions():
    empty = []
    for i in range(numberOfRooms):
        for j in range(numberOfTimeslots):
            if timetable[(i, j)] is None:
                empty.append((i, j))
    return empty


def getCourseFromCourseName(courseName):
    """
    returns the course given by the course name
    """
    return courses[courseNameToIndex[courseName]]


##DEBUG
print(header)
# print(courses)
# print(courses)
# print(rooms)
# print(roomIndexToName)
# print(curricula)
# # print(unavailability_constraints_org)
# print(unavailability_constraints)
# print(room_constraints)
# print(mapTimeslotToDayAndPeriod)

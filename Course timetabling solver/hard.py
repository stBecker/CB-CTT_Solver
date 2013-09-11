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

import math

import data

# hard constraint: Availability
def teacherIsAvailable(event, timeslot):
    """
    return True if the teacher of the course is available in the timeslot
    """
    if event is None:
        return True

    for constraint in data.unavailability_constraints:
        if event.id == constraint.courseID and timeslot == constraint.timeslot:
            return False
    return True


# hard constraint: Lectures (part 2 of 2)
def timeslotHasSameLecture(event, timeslot):
    """
    checks if a lecture of the same course is already assigned to this timeslot,
    returns True if there is already a lecture of the course in this timeslot
    """
    if event is None:
        return False

    for room in range(data.numberOfRooms):
        if not data.timetable[(room, timeslot)] is None:
            if data.timetable[(room, timeslot)].id == event.id:
                return True
    return False


def timeslotHasSameTeacher(event, timeslot):
    """
    checks if a course with the same teacher is already assigned to this timeslot,
    returns True if there is
    """
    if event is None:
        return False

    for room in range(data.numberOfRooms):
        currentEv = data.timetable[(room, timeslot)] # is the current course also taught by this teacher?
        if not currentEv is None:
            if currentEv.id in data.teachers[event.teacher]:
                return True
    return False


def timeslotHasSameCurriculum(event, timeslot):
    """
    checks if a course in the same timeslot is part of the same curriculum
    returns True if it is
    """
    if event is None:
        return False

    curriculaOfEvent = data.coursesToCurricula[event.id]   # which curricula is this course part of?
    for room in range(data.numberOfRooms):
        currentEv = data.timetable[(room, timeslot)]
        if not currentEv is None:
            for cu in curriculaOfEvent:    # checks whether the current course is also part of the same curriculum
                if currentEv.id in data.curriculaToCourses[cu]:
                    return True
    return False


def assignCourseToPosition(course, position):
    """
    assign the course to the position in the timetable
    """
    # if data.timetable[position] is None and courseFitsIntoTimeslot(course, position[1]):
    data.timetable[position] = course
    data.emptyPositions.remove(position)
    data.forbiddenPositions.append(position)


def removeCourseAtPosition(position):
    """
    remove the course which was assigned at the position from the timetable
    and add it to unassigned events
    returns the removed course
    """
    ev = data.timetable[position]
    if not ev is None:
        data.timetable[position] = None
        data.emptyPositions.append(position)

    return ev


def courseFitsIntoTimeslot(course, timeslot):
    return not timeslotHasSameLecture(course, timeslot) and teacherIsAvailable(course, timeslot) \
               and not timeslotHasSameTeacher(course, timeslot) and not timeslotHasSameCurriculum(course, timeslot)


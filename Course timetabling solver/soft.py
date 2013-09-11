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

import data
import hard




# Soft Constraint: RoomCapacity
def roomCapacity(course, room):
    """
    returns the penalty of the RoomCapacity soft constraint for a single room
    """
    requiredSize = course.num_students
    capacity = data.rooms[room].capacity
    return max((requiredSize - capacity) * data.RoomCapacityPenalty, 0)


def courseFitsIntoPosition(course, position):
    room, ts = position
    return hard.courseFitsIntoTimeslot(course, ts) and roomCapacity(course, room) == 0


def roomCapacityTimeslot(event, timeslot):
    """
    returns the penalty of the RoomCapacity soft constraint for a single timeslot
    """
    penalty = 0
    for r in range(data.numberOfRooms):
        ev = data.timetable[(r, timeslot)]
        if ev is not None and ev.id == event.id:
            penalty += roomCapacity(event, r)

    return penalty


def roomCapacityAll():
    """
    For each lecture, the number of students that attend the course must
    be less or equal than the number of seats of all the rooms that host its lectures.

    returns the total penalty for all events in the timetable
    """
    mapping = {}
    for pos in data.timetable.keys():
        ev = data.timetable[pos]
        if ev is not None:
            try:
                mapping[ev.id] += roomCapacity(ev, pos[0])
            except:
                mapping[ev.id] = roomCapacity(ev, pos[0])

    penalty = 0
    for val in mapping.values():
        penalty += val
    return penalty


def minWorkingDays(event):
    """
    The lectures of each course must be spread into the given minimum
    number of days. Each day below the minimum counts as 1 violation.

    check for each timeslot that an event of the course is assigned to the timeslot at least once,
    counts the number of timeslots that have at least one occurrence of the course

    returns the minWorkingDays penalty for the course
    """
    working_days = 0
    for day in data.days:
        for ts in day:
            if hard.timeslotHasSameLecture(event, ts):
                working_days += 1
                break

    return max(event.minWorkingDays - working_days, 0) * data.MinWorkingDays


def isolatedLectures(curriculum):
    """
    Lectures belonging to a curriculum should be adjacent to each other
    (i.e., in consecutive periods). For a given curriculum we
    account for a violation every time there is one lecture not adjacent to any other
    lecture within the same day. Each isolated lecture in a curriculum counts as 1 violation.

    checks for each timeslot, whether a course which is part of the curriculum is scheduled to this timeslot;
    creates a mapping: [True, False, False,....] where True means
    a course of the curriculum exists in the respective timeslot

    returns the penalty
    """
    mapping = []
    courses_with_curriculum = data.curriculaToCourses[curriculum.id]

    for day in data.days:
        daily = []
        for ts in day:
            # check if any of the courses of the curriculum exists in the timeslot
            if any([hard.timeslotHasSameLecture(data.getCourseFromCourseName(ev), ts) for ev in
                    courses_with_curriculum]):
                daily.append(True)
            else:
                daily.append(False)
        mapping.append(daily)

    penalty = 0
    # check for any day if an isolated lecture occurs
    for day in mapping:
        for i, timeslot_has_relevant_lecture in enumerate(day):
            if timeslot_has_relevant_lecture:
                # account for first and last timeslot of the day
                if i == 0:
                    previous_has_relevant_lecture = False
                else:
                    previous_has_relevant_lecture = day[i - 1]

                try:
                    following_has_relevant_lecture = day[i + 1]
                except:
                    following_has_relevant_lecture = False

                if not (previous_has_relevant_lecture or following_has_relevant_lecture):
                    penalty += 1

    return penalty * data.IsolatedLectures


def roomStability(event):
    """
    All lectures of a course should be given in the same room. Each distinct
    room used for the lectures of a course, but the ﬁrst, counts as 1 violation.

    returns the penalty
    """
    penalty = 0
    used_rooms = []
    for pos, ev in data.timetable.items():
        if ev is not None and ev.id == event.id:
            room = pos[0]
            if room not in used_rooms:
                used_rooms.append(room)
                penalty += 1

    # substract 1 for the first room that has been used
    penalty -= 1

    return penalty * data.RoomStability


def totalCostTimetable():
    """
    returns the total cost of the timetable
    """
    total_cost = roomCapacityAll()
    for course in data.courses:
        total_cost += minWorkingDays(course)
        total_cost += roomStability(course)
    for cu in data.curricula:
        total_cost += isolatedLectures(cu)

    return total_cost



    # tc=totalCostTimetable()
    # print("total cost: "+str(tc))
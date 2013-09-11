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

import random
import time
import math

# import cProfile

import initialisation
import data
import hard
import soft
import misc


def computeAvailableTimeslots(course, listOfTimeslots=False):
    """
    returns a list and the total number of available timeslots for the course
    """
    if listOfTimeslots:
        count = 0
        ts_list = []
        for i in range(data.numberOfTimeslots):
            if hard.courseFitsIntoTimeslot(course, i):
                count += 1
                ts_list.append(i)
        return count, ts_list
    else:
        count = 0
        for i in range(data.numberOfTimeslots):
            if hard.courseFitsIntoTimeslot(course, i):
                count += 1
        return count


def getEventRanking1(ranking, num_lectures):
    for ev in data.events:
        apd = computeAvailableTimeslots(ev)
        nl = num_lectures[ev.id]
        rank = apd / math.sqrt(nl)
        ranking[ev.id].append(rank)


def computeAvailablePositions(course):
    """
    returns the total number of available positions for the course
    """
    count = 0
    for pos in data.emptyPositions:
        if soft.courseFitsIntoPosition(course, pos):
            count += 1
    return count


def getEventRanking2(ranking, num_lectures):
    for ev in data.events:
        aps = computeAvailablePositions(ev)
        nl = num_lectures[ev.id]
        rank = aps * math.sqrt(nl)
        ranking[ev.id].append(rank)


def coursesHaveSameTeacher(course1, course2):
    return course1.teacher == course2.teacher


def coursesHaveStudentsInCommon(course1, course2):
    curriculaOfCourse1 = data.coursesToCurricula[course1.id]
    for cu in curriculaOfCourse1:
        if course2.id in data.curriculaToCourses[cu]:
            return True
    return False


def computeNumberOfCoursesWithCommonStudentsTeachers(course, courses):
    """
    returns the number of courses that have either the same teacher or common students
    as the course
    """
    count = 0
    for c in courses:
        if c != course:
            if coursesHaveSameTeacher(course, c) or coursesHaveStudentsInCommon(course, c):
                count += 1
    return count


def getEventRanking3(ranking):
    for ev in data.events:
        rank = computeNumberOfCoursesWithCommonStudentsTeachers(ev, data.events)
        ranking[ev.id].append(rank)


def countUnassignedLectures():
    counter = {}
    for event in data.events:
        try:
            counter[event.id] += 1
        except:
            counter[event.id] = 1
    return counter


def orderEventsByPriority():
    """
    order the events in unassignedEvents by a heuristic
    """
    ranking = {}
    for ev in data.events:
        ranking[ev.id] = []
    num_lectures = countUnassignedLectures()
    getEventRanking1(ranking, num_lectures)
    getEventRanking2(ranking, num_lectures)
    getEventRanking3(ranking)
    data.events.sort(key=lambda ev: ranking[ev.id], reverse=True)


def orderPositionsByPriority(event):
    """
    returns a list of feasible positions
    """
    good_pos = []
    feasible_pos = []
    for pos in data.emptyPositions:
        if soft.courseFitsIntoPosition(event, pos):
            good_pos.append(pos)
        elif hard.courseFitsIntoTimeslot(event, pos[1]):
            # compute the penalty for room capacity
            rcap = soft.roomCapacity(event, pos[0])
            feasible_pos.append((rcap, pos))
            # sort the feasible positions by their penalty
    feasible_pos.sort()
    feasible_pos2 = [pos for (rcap, pos) in feasible_pos]
    # mix it up a bit more
    random.shuffle(good_pos)
    all_pos = good_pos + feasible_pos2
    return all_pos


def constructTimetable():
    """
    constructs a feasible solution or a partially feasible solution; terminates if no solution is found after 10 seconds
    adapted from Lü, Hao (2010)
    returns distance to feasibility
    """
    startingTime = time.clock()
    # it=iter(range(100))
    it = 0
    while (len(data.events) > 0 or len(
            data.unplacedEvents) > 0) and it < 1: #time.clock()-startingTime < initialisation.TL_construction:

        it += 1

        # display current cost every 5 seconds
        # if time.clock() - startingTime > 5:
        #     startingTime += 5
        #     print(len(data.events))

        orderEventsByPriority()
        num_events = len(data.events)
        for i in range(num_events):
            ev = data.events.pop()
            list_positions = orderPositionsByPriority(ev)
            # if there are no feasible positions left, move event from unassigned to unplaced
            if len(list_positions) == 0:
                data.unplacedEvents.append(ev)
            else:
                hard.assignCourseToPosition(ev, list_positions[0])

        num_unplaced = len(data.unplacedEvents)
        random.shuffle(data.unplacedEvents)
        new_positions = []

        for i in range(num_unplaced):
            pos = random.choice(data.forbiddenPositions)
            ev = hard.removeCourseAtPosition(pos)
            data.forbiddenPositions.remove(pos)
            data.events.append(ev)
            new_positions.append(pos)

        for i in range(num_unplaced):
            unplEv = data.unplacedEvents.pop()
            assigned = False
            for pos in new_positions:
                if hard.courseFitsIntoTimeslot(unplEv, pos[1]):
                    hard.assignCourseToPosition(unplEv, pos)
                    new_positions.remove(pos)
                    assigned = True
                    break
            if not assigned:
                data.events.append(unplEv)

    return len(data.events)


# cProfile.run( "constructTimetable()")

construction_time, distanceToFeasibility = misc.timedcall(constructTimetable)

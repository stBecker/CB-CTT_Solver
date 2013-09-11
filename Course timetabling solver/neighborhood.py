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

import data
import hard


def randomChose2timeslots():
    """
    returns 2 randomly chosen timeslots
    """
    ts1 = random.randrange(data.numberOfTimeslots)
    ts2 = random.randrange(data.numberOfTimeslots)
    # make sure both random timeslots are different from each other
    while ts1 == ts2:
        ts2 = random.randrange(data.numberOfTimeslots)
    return ts1, ts2


def randomChose2rooms(rooms_are_different=True):
    """
    returns 2 randomly chosen rooms
    """
    r1 = random.randrange(data.numberOfRooms)
    r2 = random.randrange(data.numberOfRooms)
    # make sure both random rooms are different from each other
    if rooms_are_different:
        while r1 == r2:
            r2 = random.randrange(data.numberOfRooms)
    return r1, r2


def randomChose2positions():
    """
    returns 2 randomly chosen positions
    """
    r1, r2 = randomChose2rooms(False)
    t1, t2 = randomChose2timeslots()

    return (r1, t1), (r2, t2)


def swap2timeslots(ts1, ts2, preserve_feasibility=True):
    """
    swaps 2 timeslots in the timetable
    preserve_feasibility ensures, that only those moves are allowed, which do
    not violate any unavailability constraints

    returns 3 variables:
    returns True if feasibility is preserved;
    returns a backup of the events in the first timeslot and the second timeslot
    """
    events_in_ts1 = [data.timetable[(i, ts1)] for i in range(data.numberOfRooms)]
    events_in_ts2 = [data.timetable[(i, ts2)] for i in range(data.numberOfRooms)]

    if preserve_feasibility:
        # checks if no unavailability constraints are violated by the swap
        for ev in events_in_ts1:
            if not ev is None:
                if not hard.teacherIsAvailable(ev, ts2):
                    return False, [], []

        for ev in events_in_ts2:
            if not ev is None:
                if not hard.teacherIsAvailable(ev, ts1):
                    return False, [], []

    if not preserve_feasibility:
        for i, ev in enumerate(events_in_ts1):
            # data.timetable[(i, ts1)] = None
            # data.emptyPositions.append(position)
            hard.removeCourseAtPosition((i, ts1))

        for i, ev in enumerate(events_in_ts2):
            hard.removeCourseAtPosition((i, ts2))

        for i, ev in enumerate(events_in_ts1):
            if not ev is None:
                if hard.courseFitsIntoTimeslot(ev, ts2):
                    hard.assignCourseToPosition(ev, (i, ts2))
                else:
                    data.events.append(ev)

        for i, ev in enumerate(events_in_ts2):
            if not ev is None:
                if hard.courseFitsIntoTimeslot(ev, ts1):
                    hard.assignCourseToPosition(ev, (i, ts1))
                else:
                    data.events.append(ev)

                    # for i, ev in enumerate(events_in_ts2):
                    #     hard.assignCourseToPosition(ev, (i, ts1))

    else:
        for i, ev in enumerate(events_in_ts1):
            data.timetable[(i, ts2)] = ev

        for i, ev in enumerate(events_in_ts2):
            data.timetable[(i, ts1)] = ev

    return True, events_in_ts1, events_in_ts2


def swap2eventPositions(pos1, pos2, preserve_feasibility=True):
    """
    swaps the positions of 2 events in the timetable
    preserve_feasibility ensures, that only those moves are allowed, which do
    not violate any hard constraints

    returns True if feasibility is preserved;
    returns 2 tuples:
    returns a backup of the original positions of both events
    """
    event_in_pos1 = data.timetable[pos1]
    event_in_pos2 = data.timetable[pos2]
    # print(event_in_pos2)
    # print(event_in_pos1)
    # print(pos1,pos2)

    # check if the events are different
    if (event_in_pos1 is None and event_in_pos2 is None) or event_in_pos1 == event_in_pos2:
        return False, (None, None), (None, None)

    if preserve_feasibility:
        # checks if the events can be feasibly assigned to the other position
        # the possible new position is made empty, before it can be checked if the event can be assigned to this timeslot
        if not event_in_pos1 is None:
            data.timetable[pos2] = None
            assignmentPossible = hard.courseFitsIntoTimeslot(event_in_pos1, pos2[1])
            data.timetable[pos2] = event_in_pos2
            if not assignmentPossible:
                return False, (None, None), (None, None)
        if not event_in_pos2 is None:
            data.timetable[pos1] = None
            assignmentPossible = hard.courseFitsIntoTimeslot(event_in_pos2, pos1[1])
            data.timetable[pos1] = event_in_pos1
            if not assignmentPossible:
                return False, (None, None), (None, None)

    # swap the positions
    if not preserve_feasibility:
        hard.removeCourseAtPosition(pos1)
        hard.removeCourseAtPosition(pos2)
        if not event_in_pos1 is None:
            if hard.courseFitsIntoTimeslot(event_in_pos1, pos2[1]):
                hard.assignCourseToPosition(event_in_pos1, pos2)
            else:
                data.events.append(event_in_pos1)
        if not event_in_pos2 is None:
            if hard.courseFitsIntoTimeslot(event_in_pos2, pos1[1]):
                hard.assignCourseToPosition(event_in_pos2, pos1)
            else:
                data.events.append(event_in_pos2)

    else:
        data.timetable[pos1] = event_in_pos2
        data.timetable[pos2] = event_in_pos1

    return True, (pos1, event_in_pos1), (pos2, event_in_pos2)


def swap2eventRooms(r1, r2, timeslot):
    """
    swaps the rooms of 2 events in the same timeslot;
    feasibility is preserved by design!

    returns True if succesful
    returns 2 tuples:
    returns a backup of the original rooms of both events
    """
    event_in_r1 = data.timetable[(r1, timeslot)]
    event_in_r2 = data.timetable[(r2, timeslot)]

    if (event_in_r1 is None and event_in_r2 is None) or event_in_r1 == event_in_r2:
        return False, (None, None), (None, None)

    # swap the rooms
    # hard.removeCourseAtPosition((r1,timeslot))
    # hard.removeCourseAtPosition((r2,timeslot))
    # hard.assignCourseToPosition(event_in_r2,(r1, timeslot))
    # hard.assignCourseToPosition(event_in_r1,(r2, timeslot))

    data.timetable[(r1, timeslot)] = event_in_r2
    data.timetable[(r2, timeslot)] = event_in_r1

    return True, (r1, event_in_r1), (r2, event_in_r2)


def reverseSwapTimeslots(events_in_ts1, events_in_ts2, ts1, ts2):
    """
    reverse the swap of 2 timeslots

    input:
    2 lists of events
    2 timeslots
    """

    for i, ev in enumerate(events_in_ts1):
        data.timetable[(i, ts1)] = ev

    for i, ev in enumerate(events_in_ts2):
        data.timetable[(i, ts2)] = ev


def reverseSwapRooms(room_event1, room_event2, timeslot):
    """
    reverse the previous swap of 2 rooms within a timeslot

    input:
    2 tuples of (room,event)
    """
    r1, event1 = room_event1
    r2, event2 = room_event2

    data.timetable[(r1, timeslot)] = event1
    data.timetable[(r2, timeslot)] = event2


def reverseSwapPositions(pos_event1, pos_event2):
    """
    reverse the swap of the positions of 2 events

    input:
    2 tuples of (position,event)
    """
    pos1, event1 = pos_event1
    pos2, event2 = pos_event2

    data.timetable[pos1] = event1
    data.timetable[pos2] = event2
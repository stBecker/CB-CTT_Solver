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
import copy
import time
import random

import initialisation
import misc
import data
import neighborhood
import hard
import construct


best_distance = len(data.events)
best_feasible_tt = copy.deepcopy(data.timetable)

last_distance = best_distance


def swapTimeslots(T, tabu=False):
    """
    relevant costs for time slot swapping:
    Isolated Lectures, Min working days

    default mode: simulated annealing
    extra mode: tabu search
    """
    global last_distance, best_feasible_tt, best_distance
    ts1, ts2 = neighborhood.randomChose2timeslots()

    if tabu:
        # if the move is on the tabu list, abort
        if (ts1, ts2) in T or (ts2, ts1) in T:
            return False
        else:
            T.append((ts1, ts2))
            T.append((ts2, ts1))

    # init_cost=0
    # for course in data.courses:
    #     init_cost+=soft.minWorkingDays(course)
    # for cu in data.curricula:
    #     init_cost+=soft.isolatedLectures(cu)

    backupEvents = copy.copy(data.events)
    # backupUnplaced = copy.copy(data.unplacedEvents)
    backupEmptyPos = copy.copy(data.emptyPositions)
    backupTT = copy.deepcopy(data.timetable)

    successful, backup1, backup2 = neighborhood.swap2timeslots(ts1, ts2, preserve_feasibility=False)

    if not successful:
        return False


    # check if the new assignments are feasible; if not remove the event
    # backup1 = the events originally in time slot 1, now in time slot 2;
    # check if their placement in time slot 2 is feasible
    # if not unassign from timetable
    # for i, ev in enumerate(backup1):
    #     if ev is not None:
    #         if not hard.courseFitsIntoTimeslot(ev, ts2):
    #             hard.removeCourseAtPosition((i, ts2))
    #             data.events.append(ev)
    #
    # for i, ev in enumerate(backup2):
    #     if ev is not None:
    #         if not hard.courseFitsIntoTimeslot(ev, ts1):
    #             hard.removeCourseAtPosition((i, ts1))
    #             data.events.append(ev)

    # try assigning the unplaced courses to empty positions
    random.shuffle(data.events)
    events2 = copy.copy(data.events)

    for ev in data.events:
        for pos in data.emptyPositions:
            if hard.courseFitsIntoTimeslot(ev, pos[1]):
                hard.assignCourseToPosition(ev, pos)
                events2.remove(ev)
                break

    # new_cost=0
    # for course in data.courses:
    #     init_cost+=soft.minWorkingDays(course)
    # for cu in data.curricula:
    #     init_cost+=soft.isolatedLectures(cu)
    #
    # # compute the resulting cost change
    # delta_e=new_cost-init_cost

    data.events = events2
    distance = len(data.events)
    delta_e = distance - last_distance
    # print(delta_e)

    if tabu:
        if delta_e > 0:
            # neighborhood.reverseSwapTimeslots(backup1, backup2, ts1, ts2)
            data.events = backupEvents
            # data.unplacedEvents = backupUnplaced
            data.emptyPositions = backupEmptyPos
            data.timetable = backupTT
            return False
    else:
        # check if the new timetable is worse than the previous one
        # undo a worse timetable with probability 1 - exp(-delta_e/T)
        # if the timetable is not accepted, undo the previous neighborhood move
        # restore the previous state
        if delta_e > 0 and random.random() > math.exp(-delta_e / T):
            # neighborhood.reverseSwapTimeslots(backup1, backup2, ts1, ts2)
            data.events = backupEvents
            # data.unplacedEvents = backupUnplaced
            data.emptyPositions = backupEmptyPos
            data.timetable = backupTT
            return False

    # update the last cost value
    last_distance = distance

    # check if a new best has been found and save the best timetable
    if distance < best_distance:
        best_feasible_tt = copy.deepcopy(data.timetable)
        best_distance = distance
        # misc.displayTimetable(data.timetable)

    return True


def swapPositions(T, tabu=False):
    """
    relevant costs for time slot swapping:
    Isolated Lectures, Min working days, Room capacity, room stability

    default mode: simulated annealing
    extra mode: tabu search
    """
    global last_distance, best_feasible_tt, best_distance
    pos1, pos2 = neighborhood.randomChose2positions()

    if tabu:
        # if the move is on the tabu list, abort
        if (pos1, pos2) in T or (pos2, pos1) in T:
            return False
        else:
            T.append((pos1, pos2))
            T.append((pos2, pos1))

    backupEvents = copy.copy(data.events)
    # backupUnplaced = copy.copy(data.unplacedEvents)
    backupEmptyPos = copy.copy(data.emptyPositions)
    backupTT = copy.deepcopy(data.timetable)

    successful, backup1, backup2 = neighborhood.swap2eventPositions(pos1, pos2, preserve_feasibility=False)

    if not successful:
        return False

    # check if the new assignments are feasible; if not remove the event
    # backup1[1] is the event that was assigned to pos2
    # if not hard.courseFitsIntoTimeslot(backup1[1], pos2[1]):
    #     hard.removeCourseAtPosition(pos2)
    #     data.events.append(backup1[1])
    #
    # if not hard.courseFitsIntoTimeslot(backup2[1], pos1[1]):
    #     hard.removeCourseAtPosition(pos1)
    #     data.events.append(backup2[1])


    # try assigning the unplaced courses to empty positions
    random.shuffle(data.events)
    events2 = copy.copy(data.events)

    for ev in data.events:
        for pos in data.emptyPositions:
            if hard.courseFitsIntoTimeslot(ev, pos[1]):
                hard.assignCourseToPosition(ev, pos)
                events2.remove(ev)
                break

    data.events = events2
    distance = len(data.events)
    delta_e = distance - last_distance
    # print(delta_e)

    if tabu:
        if delta_e > 0:
            # neighborhood.reverseSwapPositions(backup1, backup2)
            data.events = backupEvents
            # data.unplacedEvents = backupUnplaced
            data.emptyPositions = backupEmptyPos
            data.timetable = backupTT
            return False
    else:
        # check if the new timetable is worse than the previous one
        # undo a worse timetable with probability 1 - exp(-delta_e/T)
        # if the timetable is not accepted, undo the previous neighborhood move
        # restore the previous state
        if delta_e > 0 and random.random() > math.exp(-delta_e / T):
            # neighborhood.reverseSwapPositions(backup1, backup2)
            data.events = backupEvents
            # data.unplacedEvents = backupUnplaced
            data.emptyPositions = backupEmptyPos
            data.timetable = backupTT
            return False

    # update the last cost value
    last_distance = distance
    # misc.displayTimetable(data.timetable)

    # check if a new best has been found and save the best timetable
    if distance < best_distance:
        best_feasible_tt = copy.deepcopy(data.timetable)
        best_distance = distance
        # misc.displayTimetable(data.timetable)

    return True


def tabu_search_hard(tabu_length):
    """
    reduce the distance to feasibility of the timetable
    runs until the time limit is reached or a perfect solution is found

    returns smallest distance and best timetable
    """
    startingTime = time.clock()

    tabu_timeslots = []
    tabu_positions = []

    iterations = 0

    while best_distance > 0 and time.clock() - data.starting_time < initialisation.max_runtime: #initialisation.TL_feasibility: #iterations < 30000:

        # iterations += 1

        # display current cost every 5 seconds
        if time.clock() - startingTime > 5:
            startingTime += 5
            initialisation.distance_over_time.append(best_distance)
            # print("Current distance: " + str(best_distance))

        # update the tabu lists
        if len(tabu_timeslots) > tabu_length:
            tabu_timeslots.pop(0)

        if len(tabu_positions) > tabu_length:
            tabu_positions.pop(0)

        # select a random neighborhood move
        x = random.randrange(2)

        # test: neighborhood
        # x = initialisation.nh_f
        # if x == 2:
        #     x = random.randrange(2)

        if x == 0:
            change = swapTimeslots(tabu_timeslots, tabu=True)
        else:
            change = swapPositions(tabu_positions, tabu=True)


    # print("num iterations: ", str(iterations))
    return (best_distance, best_feasible_tt)


def simulated_annealing_hard(Tmax, Tmin, steps):
    """
    reduce the distance to feasibility of the timetable
    runs until the time limit is reached or a perfect solution is found

    returns smallest distance and best timetable
    """
    startingTime = time.clock()
    # while (time.clock() - startingTime) < 15:

    step = 0
    # Precompute factor for exponential cooling from Tmax to Tmin
    Tfactor = -math.log(float(Tmax) / Tmin)

    no_improvement = 0

    iterations = 0

    while best_distance > 0 and time.clock() - startingTime < initialisation.TL_feasibility: #iterations < 30000:# time.clock() < data.timelimit:
        # iterations += 1
        # misc.displayTimetable(data.timetable)
        #if local optima has been found, reset temperature
        if no_improvement > 10:
            step = 0

        # display current cost every 5 seconds
        # if time.clock() - startingTime > 5:
        #     startingTime += 5
        #     print("Current distance: " + str(last_distance))

        T = Tmax * math.exp(Tfactor * step / steps)

        if T > Tmin:
            step += 1

        # select a random neighborhood move
        x = random.randrange(2)

        if x == 0:
            change = swapTimeslots(T)
        else:
            change = swapPositions(T)

        # check if a local optimum has been found
        if not change:
            no_improvement += 1
        else:
            no_improvement = 0

    return (best_distance, best_feasible_tt)


if construct.distanceToFeasibility > 0:
    if initialisation.searchType == "TS":
        feasibility_time, tmp = misc.timedcall(tabu_search_hard, initialisation.tabu_length)
        best_distance, best_feasible_tt = tmp
        data.timetable = best_feasible_tt
    else:
        feasibility_time, tmp = misc.timedcall(simulated_annealing_hard, initialisation.Tmax, initialisation.Tmin,
                                               initialisation.steps)
        best_distance, best_feasible_tt = tmp
        data.timetable = best_feasible_tt
else:
    best_distance = construct.distanceToFeasibility
    feasibility_time = 0
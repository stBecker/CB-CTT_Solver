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
import copy
import math

import data
import neighborhood
import soft
import initialisation
import misc
# import feasibility


best_cost = soft.totalCostTimetable()
best_feasible_tt = copy.deepcopy(data.timetable)

last_cost = best_cost

# misc.displayTimetable(data.timetable)


def swapTimeslots(T, tabu=False):
    """
    relevant costs for time slot swapping:
    Isolated Lectures, Min working days

    default mode: simulated annealing
    extra mode: tabu search
    """
    global last_cost, best_feasible_tt, best_cost
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

    successful, backup1, backup2 = neighborhood.swap2timeslots(ts1, ts2, preserve_feasibility=True)

    if not successful:
        return False

    # new_cost=0
    # for course in data.courses:
    #     init_cost+=soft.minWorkingDays(course)
    # for cu in data.curricula:
    #     init_cost+=soft.isolatedLectures(cu)
    #
    # # compute the resulting cost change
    # delta_e=new_cost-init_cost

    total_cost = soft.totalCostTimetable()
    delta_e = total_cost - last_cost

    if tabu:
        if delta_e > 0:
            neighborhood.reverseSwapTimeslots(backup1, backup2, ts1, ts2)
            return False
    else:
        # check if the new timetable is worse than the previous one
        # undo a worse timetable with probability 1 - exp(-delta_e/T)
        # if the timetable is not accepted, undo the previous neighborhood move
        # restore the previous state
        if delta_e > 0 and random.random() > math.exp(-delta_e / T):
            neighborhood.reverseSwapTimeslots(backup1, backup2, ts1, ts2)
            return False

    # update the last cost value
    last_cost = total_cost

    # check if a new best has been found and save the best timetable
    if total_cost < best_cost:
        best_feasible_tt = copy.deepcopy(data.timetable)
        best_cost = total_cost

    return True


def swapPositions(T, tabu=False):
    """
    relevant costs for time slot swapping:
    Isolated Lectures, Min working days, Room capacity, room stability

    default mode: simulated annealing
    extra mode: tabu search
    """
    global last_cost, best_feasible_tt, best_cost
    pos1, pos2 = neighborhood.randomChose2positions()

    if tabu:
        # if the move is on the tabu list, abort
        if (pos1, pos2) in T or (pos2, pos1) in T:
            return False
        else:
            T.append((pos1, pos2))
            T.append((pos2, pos1))

    successful, backup1, backup2 = neighborhood.swap2eventPositions(pos1, pos2)

    if not successful:
        return False

    total_cost = soft.totalCostTimetable()
    delta_e = total_cost - last_cost

    if tabu:
        if delta_e > 0:
            neighborhood.reverseSwapPositions(backup1, backup2)
            return False
    else:
        # check if the new timetable is worse than the previous one
        # undo a worse timetable with probability 1 - exp(-delta_e/T)
        # if the timetable is not accepted, undo the previous neighborhood move
        # restore the previous state
        if delta_e > 0 and random.random() > math.exp(-delta_e / T):
            neighborhood.reverseSwapPositions(backup1, backup2)
            return False

    # update the last cost value
    last_cost = total_cost

    # check if a new best has been found and save the best timetable
    if total_cost < best_cost:
        best_feasible_tt = copy.deepcopy(data.timetable)
        best_cost = total_cost

    return True


def swapRooms(T, tabu=False):
    """
    relevant costs for time slot swapping:
    Room capacity, room stability

    default mode: simulated annealing
    extra mode: tabu search
    """
    global last_cost, best_feasible_tt, best_cost
    r1, r2 = neighborhood.randomChose2rooms()
    ts = random.randrange(data.numberOfTimeslots)

    if tabu:
        # if the move is on the tabu list, abort
        if (r1, r2, ts) in T or (r2, r1, ts) in T:
            return False
        else:
            T.append((r1, r2, ts))
            T.append((r2, r1, ts))

    successful, backup1, backup2 = neighborhood.swap2eventRooms(r1, r2, ts)

    if not successful:
        return False

    total_cost = soft.totalCostTimetable()
    delta_e = total_cost - last_cost

    if tabu:
        if delta_e > 0:
            neighborhood.reverseSwapRooms(backup1, backup2, ts)
            return False
    else:
        # check if the new timetable is worse than the previous one
        # undo a worse timetable with probability 1 - exp(-delta_e/T)
        # if the timetable is not accepted, undo the previous neighborhood move
        # restore the previous state
        if delta_e > 0 and random.random() > math.exp(-delta_e / T):
            neighborhood.reverseSwapRooms(backup1, backup2, ts)
            return False

    # update the last cost value
    last_cost = total_cost

    # check if a new best has been found and save the best timetable
    if total_cost < best_cost:
        best_feasible_tt = copy.deepcopy(data.timetable)
        best_cost = total_cost
    return True


def simulated_annealing_soft(Tmax, Tmin, steps):
    """
    improve the soft constraints(total cost) of the timetable
    runs until the time limit is reached or a perfect solution is found

    returns best cost and best timetable
    """
    startingTime = time.clock()
    # while (time.clock() - startingTime) < 15:

    step = 0
    # Precompute factor for exponential cooling from Tmax to Tmin
    Tfactor = -math.log(float(Tmax) / Tmin)

    no_improvement = 0

    iterations = 0

    while best_cost > 0 and time.clock() - startingTime < initialisation.TL_improvement: # iterations < 0:
        # iterations += 1

        #if local optima has been found, reset temperature
        if no_improvement > 10:
            step = 0

        # display current cost every 5 seconds
        # if time.clock() - startingTime > 5:
        #     startingTime += 5
        #     print("Current total cost: " + str(last_cost))

        T = Tmax * math.exp(Tfactor * step / steps)

        if T > Tmin:
            step += 1

        # select a random neighborhood move
        x = random.randrange(3)
        if x == 0:
            change = swapTimeslots(T)
        elif x == 1:
            change = swapPositions(T)
        else:
            change = swapRooms(T)

        # check if a local optimum has been found
        if not change:
            no_improvement += 1
        else:
            no_improvement = 0

    return (best_cost, best_feasible_tt)


def tabu_search_soft(tabu_length):
    """
    improve the soft constraints(total cost) of the timetable
    runs until the time limit is reached or a perfect solution is found

    returns best cost and best timetable
    """
    startingTime = time.clock()

    tabu_timeslots = []
    tabu_positions = []
    tabu_rooms = []

    iterations = 0

    while best_cost > 0 and time.clock() - data.starting_time < initialisation.max_runtime: #initialisation.TL_improvement: # iterations < 0:
        # iterations += 1

        # display current cost every 5 seconds
        if time.clock() - startingTime > 10:
            startingTime += 10
            initialisation.soft_score_over_time.append(best_cost)
            # print("Current penalty: " + str(best_cost))

        if len(tabu_timeslots) > tabu_length:
            tabu_timeslots.pop(0)

        if len(tabu_rooms) > tabu_length:
            tabu_rooms.pop(0)

        if len(tabu_positions) > tabu_length:
            tabu_positions.pop(0)

        # select a random neighborhood move
        x = random.randrange(3)

        # test: neighborhood
        # x = initialisation.nh_i
        # if x == 6:
        #     # all neighborhoods
        #     x = random.choice([0, 1, 2])
        # elif x == 3:
        #     # timeslot/event
        #     x = random.choice([0, 1])
        # elif x == 4:
        #     # room/event
        #     x = random.choice([1, 2])
        # elif x == 5:
        #     # timeslot/room
        #     x = random.choice([0, 2])

        # select the neighborhood move
        if x == 0:
            change = swapTimeslots(tabu_timeslots, tabu=True)
        elif x == 1:
            change = swapPositions(tabu_positions, tabu=True)
        elif x == 2:
            change = swapRooms(tabu_rooms, tabu=True)

    return (best_cost, best_feasible_tt)


if initialisation.choice_inst != 0:
    if initialisation.improveType == "TS":
        improvement_time, tmp = misc.timedcall(tabu_search_soft, initialisation.tabu_length)
    else:
        improvement_time, tmp = misc.timedcall(simulated_annealing_soft, initialisation.Tmax, initialisation.Tmin,
                                               initialisation.steps)
    best_cost, best_tt = tmp
else:
    best_tt = best_feasible_tt
    improvement_time = 0
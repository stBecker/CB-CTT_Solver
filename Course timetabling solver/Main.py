""" Curriculum-based course timetabling solver;
    solves timetabling problems formulated in .ectt file format (http://tabu.diegm.uniud.it/ctt/)
    Copyright (C) 2013  Stephan E. Becker <BeckerErno@gmail.com>

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

import imp
import copy

import initialisation
import misc
import data
import construct
import feasibility
import improve
import validate


def promptUserForChoice():
    """
    asks the user to select an instance, returns type and number
    """
    choice_type = int(input("Select a dataset; press 0 for test or 1 for comp>>>>"))
    choice_number = int(input("Select an instance from the dataset; press 0 for toy, 1-4 for test, 1-21 for comp>>>>"))
    choice_maxtime = int(input("For how many seconds should the solver be allowed to run?>>>"))
    return choice_type, choice_number, choice_maxtime


def buildTimetable(index_set, index_instance, runtime):
    initialisation.choice_set = index_set
    initialisation.choice_inst = index_instance
    initialisation.max_runtime = runtime

    print("Processing data...")
    imp.reload(data)
    print("Constructing...")
    imp.reload(construct)
    # misc.displayTimetable(data.timetable)
    print("Achieving feasibility...")
    imp.reload(feasibility)
    print("Improving...")
    imp.reload(improve)
    print("Validating...")
    imp.reload(validate)

    misc.displayTimetable(improve.best_tt)
    for line in validate.outputList:
        print(line)
    print("distance after construction: ", str(construct.distanceToFeasibility))
    print("Construction time in seconds: " + str(construct.construction_time))
    print("Feasibility time in seconds: " + str(feasibility.feasibility_time))
    print("Improvement time in seconds: " + str(improve.improvement_time))


type, number, maxtime = promptUserForChoice()
buildTimetable(type, number, maxtime)


# buildTimetable(1, 7, 4000)

# misc.displayTimetable(solver.best_tt)

# for line in validate.outputList:
#     print(line)
# print("Construction time in seconds: " + str(solver.construction_time))
# print("Feasibility time in seconds: " + str(solver.feasibility_time))
# print("Improvement time in seconds: " + str(solver.improvement_time))

# Spec: Intel Core 2 Duo T6500 (@ 2.1 GHz, 800 MHz FSB), 4 GB DDR 3 RAM, Windows 7 x64
# ITC-2 allowed time, according to the benchmark program: 442 seconds


# for i in range(1, 5):
#     buildTimetable(0, i, 60)

# for i in range(1, 22):
#     buildTimetable(1, i, 60)



# ## parameter setting: tabu search hard
# def buildTimetable_2(index_instance,tabu_length):
#     initialisation.choice_inst = index_instance
#
#     imp.reload(feasibility)
#     print("Improving...")
#     imp.reload(improve)
#     imp.reload(solver)
#     print("Validating...")
#     imp.reload(validate)
#
#     print("tabu len: ",str(tabu_length))
#     print("hard: ",str(validate.violations))
#     print("Construction time in seconds: " + str(solver.construction_time))
#     print("Feasibility time in seconds: " + str(solver.feasibility_time))
#     print("Improvement time in seconds: " + str(solver.improvement_time))
#
#
# for instan in [1,3,4,11,18]:
#     initialisation.choice_inst = instan
#     imp.reload(data)
#     imp.reload(construct)
#     tt=copy.deepcopy(data.timetable)
#     evts=copy.copy(data.events)
#     emptypos=copy.copy(data.emptyPositions)
#     unplcevents=copy.copy(data.unplacedEvents)
#
#     for t_length in range(5,500,50):
#         initialisation.tabu_length=t_length
#         for i in range(5):
#             data.timetable=copy.deepcopy(tt)
#             data.events=copy.copy(evts)
#             data.emptyPositions=copy.copy(emptypos)
#             data.unplacedEvents=copy.copy(unplcevents)
#             buildTimetable_2(instan,t_length)




## parameter setting: tabu search hard
def buildTimetable_2(index_instance, test_para):
    initialisation.choice_inst = index_instance

    imp.reload(feasibility)
    print("Improving...")
    imp.reload(improve)
    print("Validating...")
    imp.reload(validate)

    print("parameter steps: ", str(test_para))
    print("soft: ", str(validate.totalCost))
    # print("Construction time in seconds: " + str(solver.construction_time))
    # print("Feasibility time in seconds: " + str(solver.feasibility_time))
    # print("Improvement time in seconds: " + str(solver.improvement_time))

#
# for instan in [1,3,4,11,18]:
#     initialisation.choice_inst = instan
#     imp.reload(data)
#     imp.reload(construct)
#     tt=copy.deepcopy(data.timetable)
#     evts=copy.copy(data.events)
#     emptypos=copy.copy(data.emptyPositions)
#     unplcevents=copy.copy(data.unplacedEvents)
#     print("distance to feasibility: ",str(construct.distanceToFeasibility))
#
#     for t_length in range(0,500,100):
#         initialisation.tabu_length=t_length
#         for i in range(5):
#             data.timetable=copy.deepcopy(tt)
#             data.events=copy.copy(evts)
#             data.emptyPositions=copy.copy(emptypos)
#             data.unplacedEvents=copy.copy(unplcevents)
#             buildTimetable_2(instan,t_length)



# for instan in [1,3,4,11,18]:
#     initialisation.choice_inst = instan
#     imp.reload(data)
#     imp.reload(construct)
#     tt=copy.deepcopy(data.timetable)
#     evts=copy.copy(data.events)
#     emptypos=copy.copy(data.emptyPositions)
#     unplcevents=copy.copy(data.unplacedEvents)
#     print("distance to feasibility: ",str(construct.distanceToFeasibility))
#
#     for Tmax in range(5,100,10):
#         initialisation.Tmax=Tmax
#         for i in range(3):
#             data.timetable=copy.deepcopy(tt)
#             data.events=copy.copy(evts)
#             data.emptyPositions=copy.copy(emptypos)
#             data.unplacedEvents=copy.copy(unplcevents)
#             buildTimetable_2(instan,Tmax)


# for instan in [1, 3, 4, 11, 18]:
#     initialisation.choice_inst = instan
#     imp.reload(data)
#     imp.reload(construct)
#     tt = copy.deepcopy(data.timetable)
#     evts = copy.copy(data.events)
#     emptypos = copy.copy(data.emptyPositions)
#     unplcevents = copy.copy(data.unplacedEvents)
#     print("distance to feasibility: ", str(construct.distanceToFeasibility))
#
#     for Tmin in range(1, 22, 4):
#         Tmin2 = float(Tmin) / 10
#         initialisation.Tmin = Tmin2
#         for i in range(3):
#             data.timetable = copy.deepcopy(tt)
#             data.events = copy.copy(evts)
#             data.emptyPositions = copy.copy(emptypos)
#             data.unplacedEvents = copy.copy(unplcevents)
#             buildTimetable_2(instan, Tmin2)



# for instan in [1, 3, 4, 11, 18]:
#     initialisation.choice_inst = instan
#     imp.reload(data)
#     imp.reload(construct)
#     tt = copy.deepcopy(data.timetable)
#     evts = copy.copy(data.events)
#     emptypos = copy.copy(data.emptyPositions)
#     unplcevents = copy.copy(data.unplacedEvents)
#     print("distance to feasibility: ", str(construct.distanceToFeasibility))
#
#     for steps in range(1, 102, 20):
#         initialisation.steps = steps
#         for i in range(3):
#             data.timetable = copy.deepcopy(tt)
#             data.events = copy.copy(evts)
#             data.emptyPositions = copy.copy(emptypos)
#             data.unplacedEvents = copy.copy(unplcevents)
#             buildTimetable_2(instan, steps)



def buildTimetable_3(stype):
    imp.reload(feasibility)
    print("Improving...")
    imp.reload(improve)
    print("Validating...")
    imp.reload(validate)

    print(stype)
    print("distance after construction: ", str(construct.distanceToFeasibility))
    print("new distance: ", str(feasibility.best_distance))
    print("hard: ", str(validate.violations))

    print("Construction time in seconds: " + str(construct.construction_time))
    print("Feasibility time in seconds: " + str(feasibility.feasibility_time))
    print("Improvement time in seconds: " + str(improve.improvement_time))


# buildTimetable(1, 1, 32)


# for instan in [3, 4, 8, 11, 18]:
#     initialisation.choice_inst = instan
#     imp.reload(data)
#     imp.reload(construct)
#     tt = copy.deepcopy(data.timetable)
#     evts = copy.copy(data.events)
#     emptypos = copy.copy(data.emptyPositions)
#     unplcevents = copy.copy(data.unplacedEvents)
#     print("distance to feasibility: ", str(construct.distanceToFeasibility))
#     for sType in ["SA", "TS"]:
#         initialisation.searchType = sType
#         for i in range(10):
#             data.timetable = copy.deepcopy(tt)
#             data.events = copy.copy(evts)
#             data.emptyPositions = copy.copy(emptypos)
#             data.unplacedEvents = copy.copy(unplcevents)
#             buildTimetable_3(sType)


def buildTimetable_4(s_type):
    print("Processing data...")
    imp.reload(data)
    print("Constructing...")
    imp.reload(construct)
    print("Searching feasibility...")
    imp.reload(feasibility)
    print("Improving...")
    imp.reload(improve)
    print("Validating...")
    imp.reload(validate)

    print(s_type)
    print("distance after construction: ", str(construct.distanceToFeasibility))
    print("new distance: ", str(feasibility.best_distance))
    print("hard: ", str(validate.violations))

    print("Construction time in seconds: " + str(construct.construction_time))
    print("Feasibility time in seconds: " + str(feasibility.feasibility_time))
    print("Improvement time in seconds: " + str(improve.improvement_time))


# for instan in [3, 4, 8, 11, 18]:
#     initialisation.choice_inst = instan
#     for s_type in ["SA", "TS"]:
#         initialisation.searchType = s_type
#         for i in range(30):
#             buildTimetable_4(s_type)

# for instan in [3, 4]:
#     initialisation.choice_inst = instan
#     s_type="TS"
#     for i in range(35):
#         buildTimetable_4(s_type)


# for instan in [1, 11, 18]:
#     initialisation.choice_inst = instan
#     for i in range(30):
#         imp.reload(data)
#         imp.reload(construct)
#         tt = copy.deepcopy(data.timetable)
#         evts = copy.copy(data.events)
#         emptypos = copy.copy(data.emptyPositions)
#         unplcevents = copy.copy(data.unplacedEvents)
#         print("distance to feasibility: ", str(construct.distanceToFeasibility))
#
#         for i_type in ["SA", "TS"]:
#             initialisation.improveType = i_type
#             data.timetable = copy.deepcopy(tt)
#             data.events = copy.copy(evts)
#             data.emptyPositions = copy.copy(emptypos)
#             data.unplacedEvents = copy.copy(unplcevents)
#             buildTimetable_3(i_type)

# for instan in [3,4]:
#     initialisation.choice_inst = instan
#     for tlength in [0,25,50,100,200,300,400,1000]:
#         initialisation.tabu_length=tlength
#         for i in range(30):
#             buildTimetable_4(tlength)

# for instan in range(2,8):
#     initialisation.choice_inst = instan
#     for tlength in [0,25,50,100,200,300,400,1000]:
#         initialisation.tabu_length=tlength
#         for i in range(10):
#             buildTimetable_4(tlength)
#
# for instan in [3,4]:
#     initialisation.choice_inst = instan
#     for tmax in [5,10,15]:
#         initialisation.Tmax=tmax
#         for i in range(20):
#             buildTimetable_4(tmax)


def buildTimetable_5(stype):
    print("Improving...")
    imp.reload(improve)
    print("Validating...")
    imp.reload(validate)

    print(stype)
    print("soft: ", str(validate.totalCost))
    print("Improvement time in seconds: " + str(improve.improvement_time))


# for instan in [1, 11, 18]:
#     initialisation.choice_inst = instan
#     for i in range(20):
#         imp.reload(data)
#         imp.reload(construct)
#         imp.reload(feasibility)
#         tt = copy.deepcopy(data.timetable)
#         evts = copy.copy(data.events)
#         emptypos = copy.copy(data.emptyPositions)
#         unplcevents = copy.copy(data.unplacedEvents)
#         print("distance after construction: ", str(construct.distanceToFeasibility))
#         print("Construction time in seconds: " + str(construct.construction_time))
#         print("Feasibility time in seconds: " + str(feasibility.feasibility_time))
#
#         for nh in range(7):
#             initialisation.nh_i = nh
#             data.timetable = copy.deepcopy(tt)
#             data.events = copy.copy(evts)
#             data.emptyPositions = copy.copy(emptypos)
#             data.unplacedEvents = copy.copy(unplcevents)
#             buildTimetable_5(nh)



def buildTimetable_6():
    print("Processing data...")
    imp.reload(data)
    print("Constructing...")
    imp.reload(construct)
    print("Searching feasibility...")
    imp.reload(feasibility)
    print("Improving...")
    imp.reload(improve)
    print("Validating...")
    imp.reload(validate)

    print("distance after construction: ", str(construct.distanceToFeasibility))
    print("hard: ", str(validate.violations))
    print("soft: ", str(validate.totalCost))

    print("Construction time in seconds: " + str(construct.construction_time))
    print("Feasibility time in seconds: " + str(feasibility.feasibility_time))
    print("Improvement time in seconds: " + str(improve.improvement_time))


    # for comp in range(1, 22):
    #     initialisation.choice_inst = comp
    #     for i in range(10):
    #         initialisation.distance_over_time = []
    #         initialisation.soft_score_over_time = []
    #         buildTimetable_6()
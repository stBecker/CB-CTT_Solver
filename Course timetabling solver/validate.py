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

import subprocess
import os
import datetime

import initialisation
import data

import construct
import feasibility
import improve

formulation = "UD2"

solutions_dir = os.path.join(os.path.dirname(__file__), 'solutions') + "\\"

output_file = data.header.name + "-last"
filename_last = solutions_dir + output_file + "." + formulation
filename_best = solutions_dir + data.header.name + "." + formulation
filename_lastTxt = solutions_dir + output_file + formulation + ".txt"
filename_bestTxt = solutions_dir + data.header.name + "-" + formulation + ".txt"
filename_csv = solutions_dir + "all_runs-" + formulation + ".csv"

firstRun = not os.path.exists(filename_best)

if firstRun:
    outputFilename = filename_best
else:
    outputFilename = filename_last


def output_solution(tt_dict):
    """
    produces an output file
    <CourseID> <RoomID> <Day> <Day_Period>
    """
    if firstRun:
        outputTTData = open(filename_best, "w")
    else:
        outputTTData = open(filename_last, "w")

    for period, assignedCourse in tt_dict.items():
        if assignedCourse is not None:
            roomIndex, timeslot = period
            day, period = data.convertTimeslotToDayPeriod(timeslot)
            string = "{!s} {!s} {!s} {!s}\n".format(assignedCourse.id, data.roomIndexToName[roomIndex], day, period)
            outputTTData.write(string)

    outputTTData.close()


def formatValidatorOutput(output):
    """
    returns the output as a list AND returns the total cost
    """
    outputSplit = output.splitlines()
    outputList = [line.decode("utf-8") for line in outputSplit]

    lastLine = outputList[-1].replace(",", "")
    numbers = [int(s) for s in lastLine.split() if s.isdigit()]
    if len(numbers) == 1:
        violations = 0
        totalCost = numbers[0]
    else:
        violations = numbers[0]
        totalCost = numbers[1]

    return outputList, violations, totalCost


def validate_solution():
    p = subprocess.Popen(["validator.exe",
                          formulation, data.input_file, outputFilename], stdout=subprocess.PIPE)
    out, err = p.communicate()
    outputList, violations, totalCost = formatValidatorOutput(out)
    return outputList, violations, totalCost


def writeValidationToTxt():
    """
    first line is total Cost
    rest is validator output
    """
    if firstRun:
        outputTxt = open(filename_bestTxt, "w")
    else:
        outputTxt = open(filename_lastTxt, "w")

    outputTxt.write(str(feasibility.best_distance) + "\n")
    outputTxt.write(str(violations) + "\n")
    outputTxt.write(str(totalCost) + "\n")
    for line in outputList:
        outputTxt.write(line + "\n")
    outputTxt.write("Construction time in seconds: " + str(construct.construction_time) + "\n")
    outputTxt.write("Reaching feasibility time in seconds: " + str(feasibility.feasibility_time) + "\n")
    outputTxt.write("Improvement time in seconds: " + str(improve.improvement_time))
    outputTxt.close()


def appendInfoToCSV():
    """
    append the info for the current run to a csv file
    info includes:
    Date and Time, Instance name, runtime construction, distance after construction, runtime feasibility,
    distance after feasibility, runtime improvement, number of violations, total cost, search type, improve type,
    neighborhood, distance over time, soft cost over time
    """
    now = datetime.datetime.today()

    # padding for lists
    while len(initialisation.distance_over_time) < 200:
        initialisation.distance_over_time.append(0)
    while len(initialisation.soft_score_over_time) < 200:
        initialisation.soft_score_over_time.append(0)

    info_string = "{},{},{},{},{},{},{},{},{},{},{},distance:,{},penalty:,{}\n".format(str(now), data.input_file_choice,
                                                                                       construct.construction_time,
                                                                                       construct.distanceToFeasibility,
                                                                                       feasibility.feasibility_time,
                                                                                       feasibility.best_distance,
                                                                                       improve.improvement_time,
                                                                                       violations, totalCost,
                                                                                       initialisation.searchType,
                                                                                       initialisation.improveType,
                                                                                       initialisation.distance_over_time,
                                                                                       initialisation.soft_score_over_time)

    # strip [ ] from output
    info_string = info_string.replace("[", "")
    info_string = info_string.replace("]", "")

    outputCSV = open(filename_csv, "a")
    outputCSV.write(info_string)
    outputCSV.close()


def compareResults():
    bestTTtxt = open(filename_bestTxt)
    bestDistanceToFeasibility = int(bestTTtxt.readline())
    bestViolations = int(bestTTtxt.readline())
    bestTotalCost = int(bestTTtxt.readline())
    bestTTtxt.close()

    new_best = False
    if feasibility.best_distance < bestDistanceToFeasibility:
        new_best = True
    elif feasibility.best_distance == bestDistanceToFeasibility:
        if violations < bestViolations:
            new_best = True
        elif violations == bestViolations:
            if totalCost < bestTotalCost:
                new_best = True

    if new_best:
        os.replace(filename_last, filename_best)
        os.replace(filename_lastTxt, filename_bestTxt)
        print("new best timetable, the old one has been replaced")


output_solution(improve.best_tt)
outputList, violations, totalCost = validate_solution()
writeValidationToTxt()
appendInfoToCSV()

if not firstRun:
    compareResults()
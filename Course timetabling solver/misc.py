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

import time

import data


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1 - t0, result


def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers))


def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    # Your code here.
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        t = 0.
        times = []
        while t <= n:
            times.append(timedcall(fn, *args)[0])
            t += times[-1]
    return min(times), average(times), max(times)


def displayTimetable(tt):
    """
    draw a visual timetable into the console
    """
    print("Timetable: ", data.header.name)
    [print("#", end="") for i in range(data.numberOfTimeslots)]
    print("#")
    for room in range(data.numberOfRooms):
        print("Room: ", room, end="|")
        for ts in range(data.numberOfTimeslots):
            if tt[(room, ts)] is None:
                print(repr(tt[(room, ts)]).rjust(11), end="#")
            else:
                print(repr(tt[(room, ts)].id).rjust(11), end="#")
                # [print(repr(tt[(room, ts)]).rjust(11), end="#") for ts in range(numberOfTimeslots)]
        print(".")
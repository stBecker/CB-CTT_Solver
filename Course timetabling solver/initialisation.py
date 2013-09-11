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

# import random

max_runtime = 200

# max construction currently ignored!
max_construction = 180

choice_set = 1
choice_inst = 0

Tmax = 5
Tmin = 1.3
steps = 5

tabu_length = 300

searchType = "TS"
improveType = "TS"

TL_construction = 90
# construct currently loops once!

# currently ignored
TL_feasibility = 60
TL_improvement = 30

distance_over_time = []
soft_score_over_time = []


# neighborhood feasibility; 0 = timeslot swap, 1 = event swap, 2 = random
# currently default neighborhood is 2!
nh_f = 2



# neighborhood improvement; 0 = timeslot swap, 1 = event swap, 2 = room swap, 3 = timeslot/event, 4 = room/event, 5 = timeslot/room, 6 = random
# currently default neighborhood is 6!
nh_i = 6
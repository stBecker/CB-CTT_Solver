CB-CTT_Solver
=============

Curriculum-based course timetabling solver; uses Tabu Search or Simulated Annealing


The validator was compiled using Visual Studio 2012; it might not work on all configurations of Windows.
In case the validator does not work, it needs to be recompiled using the included validator.cc source code file.

The solver was implemented in and requires an installation of Python 3.

The solver is started by executing the Main.py script found in the solver folder.
The user is then asked to choose a dataset (0 for the test dataset and 1 for the comp dataset),
to choose a test instance (a number between 1-4 when the test dataset was chosen, 1-21 when the comp
dataset was chosen or 0 to select the toy instance) and to input the maximum runtime of the solver in seconds.

Example:
"Which dataset?">>>1
"Which problem instance?">>>5
"Maximum runtime?">>>200

selects the comp dataset, instance 5 from the comp dataset and lets the solver run for 200 seconds.

Further settings can be made by overwriting the default values in the initialisation.py script.

The solution timetables produced by the solver are saved to the folder "Solutions" in the solver folder.

A detailed description of the program as well as a theoretical background to the university course timetabling
problem is given in the thesis paper: "Metaheuristic algorithms for the automated timetabling of university courses.pdf"
#!/usr/bin/env python

import numpy as np
import os
import subprocess

milestones = [2.45,2.7,3.5,4.5,5.5,7.0,9.0]

#========================================================
#USER DEFINED PARAMETERS
#========================================================
itex = 10 #number of iterations to exclude for harmonic constrained simulation
dt = 0.01 #frequency at which progress coordinate is saved (in realistic unit like ps)
tau = 11 #number of progress coordinate values saved per iteration + 1

#forward_milestone_position = 5.6
#backward_milestone_position = 3.6

for i in range(len(milestones)):

    #define the directory name for milestones
    dir_name = 'milestone_%d'%i

    #copy the generic analysis script into each directory
    if i==0 :
        os.system('cp westpa_analysis_scripts/first_milestone.py %s/analysis.py'%dir_name)
    elif i==(len(milestones)-1):
        os.system('cp westpa_analysis_scripts/last_milestone.py %s/analysis.py'%dir_name)
    else :
        os.system('cp westpa_analysis_scripts/intermediate_milestone.py %s/analysis.py'%dir_name)

    #milestone termination
    if i != len(milestones)-1:
        forward_milestone_position = milestones[i+1] 
    if i !=0:
        backward_milestone_position = milestones[i-1]
    
    #replace the user defined parameters
    subprocess.call(["sed -i 's/ITEX/%d/g' %s/analysis.py"%(itex,dir_name)], shell=True)
    subprocess.call(["sed -i 's/DT/%0.2f/g' %s/analysis.py"%(dt,dir_name)], shell=True)
    subprocess.call(["sed -i 's/TAU/%d/g' %s/analysis.py"%(tau,dir_name)], shell=True)

    if i != len(milestones)-1:
        subprocess.call(["sed -i 's/FORWARD/%0.2f/g' %s/analysis.py"%(forward_milestone_position,dir_name)], shell=True)
    if i != 0:
        subprocess.call(["sed -i 's/BACKWARD/%0.2f/g' %s/analysis.py"%(backward_milestone_position,dir_name)], shell=True)


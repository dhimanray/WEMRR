#!/usr/bin/env python

import numpy as np
import os
import subprocess

milestones = [2.4,2.6,3.6,4.6,5.6,7.0]

#========================================================
#USER DEFINED PARAMETERS
#========================================================
itex = 10 #number of iterations to exclude for harmonic constrained simulation
dt = 0.2 #frequency at which progress coordinate is saved (in realistic unit like ps)
tau = 11 #number of progress coordinate values saved per iteration + 1

#forward_milestone_position = 5.6
#backward_milestone_position = 3.6

for i in range(1,len(milestones)-1):

    #define the directory name for milestones
    dir_name = 'milestone_%d'%i

    #copy the generic analysis script into each directory
    os.system('cp generic_analysis.py %s/analysis.py'%dir_name)

    #milestone termination
    forward_milestone_position = milestones[i+1] 
    backward_milestone_position = milestones[i-1]
    
    #replace the user defined parameters
    subprocess.call(["sed -i 's/ITEX/%d/g' %s/analysis.py"%(itex,dir_name)], shell=True)
    subprocess.call(["sed -i 's/DT/%d/g' %s/analysis.py"%(dt,dir_name)], shell=True)
    subprocess.call(["sed -i 's/TAU/%d/g' %s/analysis.py"%(tau,dir_name)], shell=True)
    subprocess.call(["sed -i 's/FORWARD/%d/g' %s/analysis.py"%(forward_milestone_position,dir_name)], shell=True)
    subprocess.call(["sed -i 's/BACKWARD/%d/g' %s/analysis.py"%(backward_milestone_position,dir_name)], shell=True)


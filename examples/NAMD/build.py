#!/usr/bin/env python

import numpy as np
import os
import subprocess
import wemrr

#define milestone positions
#milestones = np.arange(2.0,5.0,1.0)
#can also be done manually
milestones = [2.45,2.7,3.5,4.5,5.5,7.0,9.0]

#define weighted ensemble bin width (list of bin widths after each milestone)
#if the n'th element of this array is x, bin width will be x between
#milestone n and n+1
we_bin_width = [0.05,0.2,0.5,0.5,0.5,0.5]
#**bin edges are automatically placed at the milestone positions**#


#harmonic restrain for equilibration
k_eq = 100.0

#harmonic restrain for WEM
k_res = 100.0

#steps of simulation
minimization_nsteps = 1000
equilibration_nsteps = 5000
equilibration_dcd_frequency = 1000
#restrained_nsteps = 100
nsteps = 100
print_frequency = 10
dcd_frequency = 100

#cfg file parameters
pcoord_len = nsteps/print_frequency + 1
n_traj_per_bin = 5
n_iterations_restrained = 10
n_iterations = 500


#generate_we_bins(milestones,milestone_index,bin_width)

wemrr.build_namd(milestones,we_bin_width,k_eq,k_res,minimization_nsteps,equilibration_nsteps,equilibration_dcd_frequency,nsteps,print_frequency,dcd_frequency,pcoord_len,n_traj_per_bin,n_iterations_restrained,n_iterations)


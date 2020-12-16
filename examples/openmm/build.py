#!/usr/bin/env python

import numpy as np
import os
import subprocess
import wemrr

#define milestone positions
#milestones = np.arange(2.0,5.0,1.0)
#can also be done manually
milestones = [2.,3.0,4.0]

#define weighted ensemble bin width
#**bin edges are automatically placed at the milestone positions**#
we_bin_width = 0.2

#harmonic restrain for equilibration
k_eq = 40.0

#harmonic restrain for WEM
k_res = 40.0

#steps of simulation
minimization_nsteps = 1000
equilibration_nsteps = 5000
nsteps = 100
print_frequency = 10
dcd_frequency = 100

#cfg file parameters
pcoord_len = nsteps/print_frequency + 1
n_traj_per_bin = 5
n_iterations_restrained = 2
n_iterations = 10


#generate_we_bins(milestones,milestone_index,bin_width)

wemrr.build_openmm(milestones,we_bin_width,k_eq,k_res,minimization_nsteps,equilibration_nsteps,nsteps,print_frequency,dcd_frequency,pcoord_len,n_traj_per_bin,n_iterations_restrained,n_iterations)


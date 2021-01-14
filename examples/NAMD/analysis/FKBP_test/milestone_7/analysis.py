#!/usr/bin/env python

#get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot as plt
import numpy as np
from wemrr import *
np.set_printoptions(threshold=np.inf)
import w_ipa
w = w_ipa.WIPI()
# At startup, it will load or run the analysis schemes specified in the configuration file (typically west.cfg)
w.main()
#w.interface = 'matplotlib'

#========================================================
#USER DEFINED PARAMETERS
#========================================================

itex = 10 #number of iterations to exclude for harmonic constrained simulation
dt = 0.20 #frequency at which progress coordinate is saved (in realistic unit like ps)
tau = 11 #number of progress coordinate values saved per iteration + 1

forward_milestone_position = 20.00
backward_milestone_position = 16.00

#=========================================================
#Compute transition statistics
#=========================================================
transitions_intermediate_milestone(w,itex,dt,tau,forward_milestone_position,backward_milestone_position)

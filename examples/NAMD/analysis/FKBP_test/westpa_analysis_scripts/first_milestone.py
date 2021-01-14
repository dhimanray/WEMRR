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

itex = ITEX #number of iterations to exclude for harmonic constrained simulation
dt = DT #frequency at which progress coordinate is saved (in realistic unit like ps)
tau = TAU #number of progress coordinate values saved per iteration + 1

forward_milestone_position = FORWARD

#=========================================================
#Compute transition statistics
#=========================================================
transitions_first_milestone(w,itex,dt,tau,forward_milestone_position)

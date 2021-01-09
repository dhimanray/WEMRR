#!/bin/bash

# Set up environment for westpa
export WEST_PYTHON=$(which python)
# Actviate a conda environment containing westpa, openmm, mdtraj;
# You may need to create this first (see install instructions)
source activate westpa-openmm  #Use the name of the environment in which WESTPA is installed
export WEST_SIM_ROOT="$PWD"
export SIM_NAME=$(basename $WEST_SIM_ROOT)

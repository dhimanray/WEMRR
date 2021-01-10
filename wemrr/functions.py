"""
functions.py
test

Handles the primary functions
"""
import numpy as np
import os
import subprocess


def canvas(with_attribution=True):
    """
    Placeholder function to show example docstring (NumPy format)

    Replace this function and doc string for your own project

    Parameters
    ----------
    with_attribution : bool, Optional, default: True
        Set whether or not to display who the quote is from

    Returns
    -------
    quote : str
        Compiled string including quote and optional attribution
    """

    quote = "The code is but a canvas to our imagination."
    if with_attribution:
        quote += "\n\t- Adapted from Henry David Thoreau"
    return quote


if __name__ == "__main__":
    # Do something if this file is invoked on its own
    print(canvas())


def generate_we_bins(milestones,milestone_index,bin_width):
    '''Generate the positions of the weighted ensemble bin edges
    around a given milestone

    milestones: Array of milestone positions

    milestone_index: Zero based ndex of the current milestone

    bin_width: width of weighted ensemble bin'''

    if milestone_index == 0:
        start = milestones[milestone_index]
        end = milestones[milestone_index+1]
        current = start
    elif milestone_index == len(milestones)-1:
        start = milestones[milestone_index-1]
        end = milestones[milestone_index]
        current = end
    else :
        start = milestones[milestone_index-1]
        end = milestones[milestone_index+1]
        current = milestones[milestone_index]

    if int((end - current)%bin_width) != 0:
        print("Milestone spacing must be integer multiple of bin width \n Error in milestone: %d"%milestone_index)
        return
    elif int((current - start)%bin_width) != 0:
        print("Milestone spacing must be integer multiple of bin width \n Error in milestone: %d"%milestone_index)
        return

    numbins = int((end - start)/bin_width)
    bin_list = [start + bin_width*i for i in range(numbins+1) ]

    #a = np.arange(start,current,bin_width)
    #b = np.arange(current,end+bin_width,bin_width)

    #print(np.concatenate((a,b)))
    #bins = np.concatenate((a,b)).tolist()

    bin_list = [round(num, 2) for num in bin_list]
    bin_list.append('inf')
    bin_list.insert(0,'-inf')

    return bin_list

#x = generate_we_bins(milestones,2,we_bin_width)
#print(str(x))

def build_namd(milestones,we_bin_width,k_eq,k_res,minimization_nsteps,equilibration_nsteps,equilibration_dcd_frequency,nsteps,print_frequency,dcd_frequency,pcoord_len,n_traj_per_bin,n_iterations_restrained,n_iterations):
    boundaries = str(['-inf',milestones[0],milestones[len(milestones)-1],'inf'])
    bound = str([milestones[0]])
    unbound = str([milestones[len(milestones)-1]])




    current = os.getcwd()

#print(current)

    for i in range(len(milestones)):

        #define the directory name for milestones
        dir_name = 'milestone_%d'%i

        #create directory
        #path = os.path.join(current,dir_name)
        #os.mkdir(path)

        #remove old milestones
        os.system('rm -r %s'%dir_name)

        #copy the template files into each directory
        os.system('cp -r template_milestone %s'%dir_name)

        #copy structure files to equilibration directory
        os.system('cp structure_files/topology.psf %s/equilibration/'%dir_name)
        os.system('cp structure_files/milestone_%d.pdb %s/equilibration/structure.pdb'%(i,dir_name))
        os.system('cp structure_files/equilibration.conf %s/equilibration/equilibration.conf'%dir_name)
        os.system('cat structure_files/colvars.in %s/equilibration/restrain.in > %s/equilibration/colvars.in'%(dir_name,dir_name))

        #copy structure files to common files directory
        os.system('cp structure_files/topology.psf %s/common_files/'%dir_name)
        os.system('cp structure_files/milestone_%d.pdb %s/common_files/structure.pdb'%(i,dir_name))
        os.system('cp structure_files/colvars.in %s/common_files/'%dir_name)
        os.system('cp structure_files/md.conf %s/common_files/md.conf'%dir_name)
        os.system('cat structure_files/colvars.in %s/common_files/restrain.in > %s/common_files/colvars_restrain.in'%(dir_name,dir_name))


        #make modifications inside each milestone directory

        #change the equilibration files
        subprocess.call(["sed -i 's/K_EQ/%0.2f/g' %s/equilibration/colvars.in"%(k_eq,dir_name)], shell=True)
        subprocess.call(["sed -i 's/X_0/%0.2f/g' %s/equilibration/colvars.in"%(milestones[i],dir_name)], shell=True)
        subprocess.call(["sed -i 's/EQBM_TIME/%d/g' %s/equilibration/colvars.in"%(equilibration_nsteps,dir_name)], shell=True)
        subprocess.call(["sed -i 's/DCD_FREQUENCY/%d/g' %s/equilibration/equilibration.conf"%(equilibration_dcd_frequency,dir_name)], shell=True)
        subprocess.call(["sed -i 's/MINIMIZATION_STEPS/%d/g' %s/equilibration/equilibration.conf"%(minimization_nsteps,dir_name)], shell=True)
        subprocess.call(["sed -i 's/EQUILIBRATION_STEPS/%d/g' %s/equilibration/equilibration.conf"%(equilibration_nsteps,dir_name)], shell=True)
        subprocess.call(["sed -i 's/TRAJ_FREQ/%d/g' %s/equilibration/colvars.in"%(print_frequency,dir_name)], shell=True)

        #change the colvars file for restrained dynamics
        subprocess.call(["sed -i 's/K_RES/%0.2f/g' %s/common_files/colvars_restrain.in"%(k_res,dir_name)], shell=True)
        subprocess.call(["sed -i 's/X_0/%0.2f/g' %s/common_files/colvars_restrain.in"%(milestones[i],dir_name)], shell=True)
        subprocess.call(["sed -i 's/TRAJ_FREQ/%d/g' %s/common_files/colvars_restrain.in"%(print_frequency,dir_name)], shell=True)

        #change the colvars file for regular dynamics
        subprocess.call(["sed -i 's/TRAJ_FREQ/%d/g' %s/common_files/colvars.in"%(print_frequency,dir_name)], shell=True)

        #change the configuration file
        subprocess.call(["sed -i 's/DCD_FREQUENCY/%d/g' %s/common_files/md.conf"%(dcd_frequency,dir_name)], shell=True)
        subprocess.call(["sed -i 's/NUM_STEPS/%d/g' %s/common_files/md.conf"%(nsteps,dir_name)], shell=True)

        #change west-restrain.cfg
        subprocess.call(["sed -i 's/PCOORD_LEN/%d/g' %s/west-restrain.cfg"%(pcoord_len,dir_name)], shell=True)
        subprocess.call(["sed -i 's/BIN_TARGET_COUNTS/%d/g' %s/west-restrain.cfg"%(n_traj_per_bin,dir_name)], shell=True)
        subprocess.call(["sed -i 's/MAX_TOTAL_ITERATIONS/%d/g' %s/west-restrain.cfg"%(n_iterations_restrained,dir_name)], shell=True)
        #Add bins and boundaries etc.
        subprocess.call(["sed -i 's/This part will be replaced by the weighted ensemble bin edges/%s/g' %s/west-restrain.cfg"%(str(generate_we_bins(milestones,i,we_bin_width)),dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-boundaries/%s/g' %s/west-restrain.cfg"%(boundaries,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-bound/%s/g' %s/west-restrain.cfg"%(bound,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-unbound/%s/g' %s/west-restrain.cfg"%(unbound,dir_name)], shell=True)



        #change west.cfg
        subprocess.call(["sed -i 's/PCOORD_LEN/%d/g' %s/west.cfg"%(pcoord_len,dir_name)], shell=True)
        subprocess.call(["sed -i 's/BIN_TARGET_COUNTS/%d/g' %s/west.cfg"%(n_traj_per_bin,dir_name)], shell=True)
        subprocess.call(["sed -i 's/MAX_TOTAL_ITERATIONS/%d/g' %s/west.cfg"%(n_iterations,dir_name)], shell=True)
        #Add bins and boundaries etc.
        subprocess.call(["sed -i 's/This part will be replaced by the weighted ensemble bin edges/%s/g' %s/west.cfg"%(str(generate_we_bins(milestones,i,we_bin_width)),dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-boundaries/%s/g' %s/west.cfg"%(boundaries,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-bound/%s/g' %s/west.cfg"%(bound,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-unbound/%s/g' %s/west.cfg"%(unbound,dir_name)], shell=True)

        #change westpa-scripts directory
        #change milestone_calculation (convert.py)
        if i == 0:
            os.system('cp %s/westpa_scripts/convert_first_milestone.py %s/westpa_scripts/convert.py'%(dir_name,dir_name))
            subprocess.call(["sed -i 's/ENDPOINT/%0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i+1],dir_name)], shell=True)
        elif i == len(milestones)-1:
            os.system('cp %s/westpa_scripts/convert_last_milestone.py %s/westpa_scripts/convert.py'%(dir_name,dir_name))
            subprocess.call(["sed -i 's/ENDPOINT/%0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i-1],dir_name)], shell=True)
        else :
            subprocess.call(["sed -i 's/ENDPOINT_1/%0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i-1],dir_name)], shell=True)
            subprocess.call(["sed -i 's/ENDPOINT_2/%0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i+1],dir_name)], shell=True)

        #change run.sh
        subprocess.call(["sed -i 's/SEGS_PER_STATE/%d/g' %s/run.sh"%(n_traj_per_bin,dir_name)], shell=True)
        subprocess.call(["sed -i 's/SEGS_PER_STATE/%d/g' %s/run.slurm"%(n_traj_per_bin,dir_name)], shell=True)


def build_openmm(milestones,we_bin_width,k_eq,k_res,minimization_nsteps,equilibration_nsteps,nsteps,print_frequency,dcd_frequency,pcoord_len,n_traj_per_bin,n_iterations_restrained,n_iterations):
    boundaries = str(['-inf',milestones[0],milestones[len(milestones)-1],'inf'])
    bound = str([milestones[0]])
    unbound = str([milestones[len(milestones)-1]])




    current = os.getcwd()

    #print(current)

    for i in range(len(milestones)):

        #define the directory name for milestones
        #dir_name = 'milestone_RC_%0.1f'%milestones[i]
        dir_name = 'milestone_%d'%i

        #create directory
        #path = os.path.join(current,dir_name)
        #os.mkdir(path)

        #remove old milestones
        os.system('rm -r %s'%dir_name)

        #copy the template files into each directory
        os.system('cp -r template_milestone %s'%dir_name)

        #copy structure files to equilibration directory
        os.system('cp structure_files/bstate.pdb %s/equilibration/'%dir_name)
        os.system('cp structure_files/milestone_%d.xml %s/equilibration/start.xml'%(i,dir_name))

        #make modifications inside each milestone directory

        #change the equilibration files
        subprocess.call(["sed -i 's/k = XX/k = %0.2f/g' %s/equilibration/equilibration.py"%(k_eq,dir_name)], shell=True)
        subprocess.call(["sed -i 's/x_0 = XX/x_0 = %0.2f/g' %s/equilibration/equilibration.py"%(milestones[i],dir_name)], shell=True)
        subprocess.call(["sed -i 's/simulation.step(XX)/simulation.step(%0.2f)/g' %s/equilibration/equilibration.py"%(equilibration_nsteps,dir_name)], shell=True)

        #change the restrained dynamics files
        subprocess.call(["sed -i 's/k = XX/k = %0.2f/g' %s/common_files/prod_restrain.py"%(k_res,dir_name)], shell=True)
        subprocess.call(["sed -i 's/x_0 = XX/x_0 = %0.2f/g' %s/common_files/prod_restrain.py"%(milestones[i],dir_name)], shell=True)
        subprocess.call(["sed -i 's/simulation.step(XX)/simulation.step(%0.2f)/g' %s/common_files/prod_restrain.py"%(nsteps,dir_name)], shell=True)
        subprocess.call(["sed -i 's/ColvarReporter1(outfilename,XX)/ColvarReporter1(outfilename,%d)/g' %s/common_files/prod_restrain.py"%(print_frequency,dir_name)], shell=True)
        subprocess.call(["sed -i 's/DCDReporter(dcdfilename, XX)/DCDReporter(dcdfilename, %d)/g' %s/common_files/prod_restrain.py"%(dcd_frequency,dir_name)], shell=True)

        #change the regular dynamics files
        subprocess.call(["sed -i 's/simulation.step(XX)/simulation.step(%0.2f)/g' %s/common_files/prod.py"%(nsteps,dir_name)], shell=True)
        subprocess.call(["sed -i 's/ColvarReporter1(outfilename,XX)/ColvarReporter1(outfilename,%d)/g' %s/common_files/prod.py"%(print_frequency,dir_name)], shell=True)
        subprocess.call(["sed -i 's/DCDReporter(dcdfilename, XX)/DCDReporter(dcdfilename, %d)/g' %s/common_files/prod.py"%(dcd_frequency,dir_name)], shell=True)

        #change west-restrain.cfg
        subprocess.call(["sed -i 's/pcoord_len: XX/pcoord_len: %d/g' %s/west-restrain.cfg"%(pcoord_len,dir_name)], shell=True)
        subprocess.call(["sed -i 's/bin_target_counts: XX/bin_target_counts: %d/g' %s/west-restrain.cfg"%(n_traj_per_bin,dir_name)], shell=True)
        subprocess.call(["sed -i 's/max_total_iterations: XX/max_total_iterations: %d/g' %s/west-restrain.cfg"%(n_iterations_restrained,dir_name)], shell=True)
        #Add bins and boundaries etc.
        subprocess.call(["sed -i 's/This part will be replaced by the weighted ensemble bin edges/%s/g' %s/west-restrain.cfg"%(str(generate_we_bins(milestones,i,we_bin_width)),dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-boundaries/%s/g' %s/west-restrain.cfg"%(boundaries,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-bound/%s/g' %s/west-restrain.cfg"%(bound,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-unbound/%s/g' %s/west-restrain.cfg"%(unbound,dir_name)], shell=True)



        #change west.cfg
        subprocess.call(["sed -i 's/pcoord_len: XX/pcoord_len: %d/g' %s/west.cfg"%(pcoord_len,dir_name)], shell=True)
        subprocess.call(["sed -i 's/bin_target_counts: XX/bin_target_counts: %d/g' %s/west.cfg"%(n_traj_per_bin,dir_name)], shell=True)
        subprocess.call(["sed -i 's/max_total_iterations: XX/max_total_iterations: %d/g' %s/west.cfg"%(n_iterations,dir_name)], shell=True)
        #Add bins and boundaries etc.
        subprocess.call(["sed -i 's/This part will be replaced by the weighted ensemble bin edges/%s/g' %s/west.cfg"%(str(generate_we_bins(milestones,i,we_bin_width)),dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-boundaries/%s/g' %s/west.cfg"%(boundaries,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-bound/%s/g' %s/west.cfg"%(bound,dir_name)], shell=True)
        subprocess.call(["sed -i 's/script-unbound/%s/g' %s/west.cfg"%(unbound,dir_name)], shell=True)

        #change westpa-scripts directory
        #change milestone_calculation (convert.py)
        if i == 0:
            os.system('cp %s/westpa_scripts/convert_first_milestone.py %s/westpa_scripts/convert.py'%(dir_name,dir_name))
            subprocess.call(["sed -i 's/endpoint = XX/endpoint = %0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i+1],dir_name)], shell=True)
        elif i == len(milestones)-1:
            os.system('cp %s/westpa_scripts/convert_last_milestone.py %s/westpa_scripts/convert.py'%(dir_name,dir_name))
            subprocess.call(["sed -i 's/endpoint = XX/endpoint = %0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i-1],dir_name)], shell=True)
        else :
            subprocess.call(["sed -i 's/endpoint1 = XX/endpoint1 = %0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i-1],dir_name)], shell=True)
            subprocess.call(["sed -i 's/endpoint2 = XX/endpoint2 = %0.2f/g' %s/westpa_scripts/convert.py"%(milestones[i+1],dir_name)], shell=True)

        #change run.sh
        subprocess.call(["sed -i 's/segs-per-state XX/segs-per-state %d/g' %s/run.sh"%(n_traj_per_bin,dir_name)], shell=True)

#THIS CODE IS AN EXAMPLE HOW TO COMPUTE VARIOUS PROPERTIES

import numpy as np
import wemrr 

milestones = [2.45,2.7,3.5,4.5,5.5,7.0,9.0]

#==================================================
#Compute steady state K and mean first passage time 
#===================================================
K,t,Nhit = wemrr.compute_kernel(milestones)

#MFPT from r=2.7 to r=7.0
print(wemrr.MFPT(K,t,1,5))

#==================================================
#Compute equilibrium K and free energy profile
#===================================================

G = wemrr.free_energy(K,t,milestones,radial=True)

print(G)

#===================================================
#Compute MFPT with error bars
#===================================================

N_total = 300
interval = 10

K_list = wemrr.Monte_Carlo_bootstrapping(N_total,K,t,Nhit,interval)

print(K_list)
mfpt_list = []
for i in range(len(K_list)):
    mfpt_list.append(wemrr.MFPT(K_list[i],t,1,5))

mfpt_list = np.array(mfpt_list)

mfpt_mean = np.mean(mfpt_list)
mfpt_std = np.std(mfpt_list)
mfpt_err = 1.96*mfpt_std #95% confidence interval

print("Mean First Passage Time = ",mfpt_mean," +/- ",mfpt_err)

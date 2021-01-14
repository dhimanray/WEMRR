import numpy as np
import wemrr as wem

milestones = [5.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0,26.0,28.0]

K,t,Nhit = wem.steady_state_kernel(milestones)

print(wem.MFPT(K,t,1,6))

Keq,t,Nhit = wem.equilibrium_kernel(milestones)

G = wem.free_energy(Keq,t,milestones,radial=True)

print(G)

import numpy as np
from scipy import linalg

def MFPT(Q,t,Ns,Nend):
    '''function to calculate Mean first passage time from a given matrix
    Input
    ------
    Q   : Transition Kernel
    t   : lifetime vector
    Ns  : Index of starting milestone (0 based)
    Nend: Index of final milestone (0 based)
    
    Returns
    ------
    tau : Mean First Passage Time'''

    K = Q.copy()
    N = len(t)

    for i in range(N):
        K[i,i] = 0.0 #make sure diagonal elements are zero
        totp = sum(K[i,:])
        for j in range(N):
            K[i,j] = K[i,j]/totp
    
    #calculate eigenvalues and eigenvectors
    eigs = linalg.eig(K,left=True,right=False)

    w = eigs[0]
    v = eigs[1]


    #sort the eigenvalues and eigenvectors
    idx = w.argsort()[::-1]
    w = w[idx]
    v = v[:,idx]

    #compute stationary flux
    q_stat = v.T[0]
  
    #compute MFPT
    tau = np.dot(q_stat[Ns:Nend+1],t[Ns:Nend+1])/q_stat[Nend]  

    return tau 

def free_energy(Q,t,mps,radial=True):
    '''function to calculate free energy profile from a given matrix
    Input
    ------
    Q      : Transition Kernel
    t      : lifetime vector
    mps    : list of milestone positions
    radial : if True, Jacobian correction for radial distance based 
             coordinate is performed
    
    Returns
    ------
    G : Array of free energy values at each milestone'''

    K = Q.copy()
    N = len(mps)

    for i in range(N):
        K[i,i] = 0.0 #make sure diagonal elements are zero
        totp = sum(K[i,:])
        for j in range(N):
            K[i,j] = K[i,j]/totp
    
    #calculate eigenvalues and eigenvectors
    eigs = linalg.eig(K,left=True,right=False)

    w = eigs[0]
    v = eigs[1]


    #sort the eigenvalues and eigenvectors
    idx = w.argsort()[::-1]
    w = w[idx]
    v = v[:,idx]
    
    #compute stationary flux
    q_stat = v.T[0]

    #compute probabilities
    p_x = np.multiply(q_stat,t)    
    p_x = p_x/sum(p_x)

    #compute free energies
    G = np.zeros(len(p_x))
    if radial == True:
        #perform Jacobian correction
        G += 2.0*np.log(np.asarray(mps))
    for i in range(len(G)):
        G[i] -= np.log(p_x[i])

    #make the minimum free energy to be zero
    G -= np.min(G)


    return G
    


def steady_state_kernel(mps):
    '''Compute the transition kernel, lifetime vector and the 
    milestone hitting statistics for the case of steady state 
    situation (for kinetics calculation).
    Will read the data from milestone_i/milestone-data.dat 
    files. i goes from 0 to N-1

    In milestone-data.dat the transition statistics is provided
    in the following order:
    MFPT_forward, MFPT_back, lifetime, forward probability, backward probability, forward count, backward count

    Input
    -----
    mps : list of milestone positions

    Returns
    -----
    K : Transition kernel
    t : lifetime vector
    Nhit : Matrix containing number of hitting points

    '''
    N = len(mps)

    K = np.zeros((N,N))

    t = np.zeros(N)

    Nhit = np.zeros((N,N))

    for i in range(N-1):
        l = np.loadtxt('milestone_%d/milestone-data.dat'%i)
        K[i,i+1] = l[3]
        Nhit[i,i+1] = l[5]
        if i!=0:
            K[i,i-1] = l[4]
            Nhit[i,i-1] = l[6]
        t[i] = l[2]
    K[N-1,0] = 1.0  #cyclic or periodic boundary condition to get steady state

    return K, t, Nhit

def equilibrium_kernel(mps):
    '''Compute the transition kernel, lifetime vector and the 
    milestone hitting statistics for the case of equilibrium 
    situation (for free energy calculation).
    Will read the data from milestone_i/milestone-data.dat 
    files. i goes from 0 to N-1

    In milestone-data.dat the transition statistics is provided
    in the following order:
    MFPT_forward, MFPT_back, lifetime, forward probability, backward probability, forward count, backward count

    Input
    -----
    mps : list of milestone positions

    Returns
    -----
    K : Transition kernel
    t : lifetime vector
    Nhit : Matrix containing number of hitting points

    '''
    N = len(mps)

    K = np.zeros((N,N))

    t = np.zeros(N)

    Nhit = np.zeros((N,N))

    for i in range(N-1):
        l = np.loadtxt('milestone_%d/milestone-data.dat'%i)
        K[i,i+1] = l[3]
        Nhit[i,i+1] = l[5]
        if i!=0:
            K[i,i-1] = l[4]
            Nhit[i,i-1] = l[6]
        t[i] = l[2]
    K[N-1,N-2] = 1.0   #reflecting boundary condition (Graziloli and Andricioaei, JCP, 149, 084103 (2018) Page 4)
    
    return K, t, Nhit

def Monte_Carlo_bootstrapping(N_total,K,t,Nhit,interval):
    '''Perform nonreversible element shift Monte Carlo to sample rate matrices

    Input
    -----
    N_total : Total number of MC moves (accepted and rejected)
    K : Transition kernel
    t : lifetime vector
    Nhit : Matrix containing number of hitting points
    interval : After how many MC moves a matrix is sampled

    Returns
    -------
    K_list : (n,N,N) dim array where n is the number of sampled
             transition kernels

    '''
    N = len(t)

    K_list = []
    
    for k in range(N_total):
        Q = K.copy()
        #construct rate matrix
        for i in range(N):
            for j in range(N):
                if t[i] != 0:
                    Q[i,j] = Q[i,j]/t[i]
        for i in range(len(Q)):
            Q[i,i] = -np.sum(Q[i])
        #choose one of the non-zero elements to change
        r1 = np.random.randint(0,N-1)
        if r1 == 0:
            Q_ab = Q[r1,r1+1]
        else :
            r2 = np.random.randint(0,1)
            if r2 == 0:
                Q_ab = Q[r1,r1-1]
            else :
                Q_ab = Q[r1,r1+1]


        delta = np.random.exponential(scale=Q_ab) - Q_ab


        log_pacc = Nhit[r1,r1+1]*np.log((Q_ab + delta)/Q_ab) - delta * t[r1]*np.sum(Nhit[r1])

        r = np.random.uniform(low=0.0,high=1.0)

        if np.log(r) < log_pacc :  #accept
            Q[r1,r1] -= delta
            if r1 == 0:
                Q[r1,r1+1] += delta
            else :
                if r2 == 0 :
                    Q[r1,r1-1] += delta

                else :
                    Q[r1,r1+1] += delta
        
        #multiply the t[i]'s to get back the sampled kernel
        sampled_K = np.zeros((N,N))
        for i in range(N):
            for j in range(N):
                if t[i] != 0:
                    sampled_K[i,j] = Q[i,j]*t[i]

        #only include after "interval" steps 
        if (k+1)%interval == 0:
            K_list.append(sampled_K)
            
        #convert from list to array before returning
        return np.array(K_list)


import numpy as np

def transitions_intermediate_milestone(w,itex,dt,tau,forward_milestone_position,backward_milestone_position):
    '''=============================
    CALCULATING MILESTONE STATISTICS
    ================================

    Computes full transition statistics for milestoning analysis

    Inputs
    -------
    w : The WESTPA simulation object
    itex : number of iterations to exclude for harmonic constrained simulation
    dt : frequency at which progress coordinate is saved (in realistic unit like ps)
    tau : number of progress coordinate values saved per iteration + 1
    forward_milestone_position :
    backward_milestone_position :


    Output files
    ------------

    milestone-data.dat : Full milestone to miletsone transition statistics
    computational_cost.txt : Total simulation cost
    flux.dat : Flux vs. time for checking convergence
    FPTD_forward.dat : First passage time distribution in forward direction
    FPTD_back.dat :First passage time distribution in backward direction

    '''

    total_iteration = w.niters

    it = [0.0 for i in range(total_iteration)]


    flux = 0.0
    flux_array = []
    sink1 = forward_milestone_position



    it_back = [0.0 for i in range(total_iteration)]
    flux_back = 0.0
    flux_back_array = []
    sink2 = backward_milestone_position

    lifetime = 0.0
    force_eval = 0.0

    count_forward = 0
    count_backward = 0

    #open file to save total computational cost
    fcost = open('computational_cost.txt','w')
    print('#iteration','#total simulation time',file=fcost)
    for i in range(total_iteration-itex):
        w.iteration = i+1+itex
        l = w.current.pcoord
        wts = w.current.weights
        #print sum(wts)
        force_eval += (tau-1)*w.current.walkers*dt
        print(w.iteration, force_eval, file=fcost)
        for j in range(len(l)):
            #print j

            if l[j][0] < sink1 and l[j][tau-1] >= sink1:
                it[i] += wts[j]
                #print wts[j], 'forwd'
                count_forward += 1
                for k in range(tau):
                    if l[j][k] < sink1 and l[j][k+1] >= sink1:
                        flux += wts[j]
                        lifetime += wts[j]*(i*(tau-1)+k)
                        break
                        #break

            if l[j][0] > sink2 and l[j][tau-1] <= sink2:
                #print l[j,0], l[j,tau-1]
                it_back[i] += wts[j]
                #print wts[j], 'backwd'
                count_backward += 1
                for k in range(tau):
                    #print 'elmnts',l[j,k]
                    if l[j][k][0] > sink2 and l[j][k+1][0] <= sink2:
                        flux_back += wts[j]
                        #print flux_back, 'fback'
                        lifetime += wts[j]*(i*(tau-1)+k)
                        break
                        #break
        flux_array.append(flux)
        flux_back_array.append(flux_back)
    flux = flux/((total_iteration-itex)*(tau-1))
    flux_back = flux_back/((total_iteration-itex)*(tau-1))

    fcost.close()


    f1 = open('milestone-data.dat','w')
    print("#MFPT  #MFPT_back  #lifetime  #forward probability  #backward probability #forward count #backward count",file=f1)
    print(1./flux, 1./flux_back, lifetime, sum(it), sum(it_back), count_forward, count_backward, file=f1)
    f1.close()




    #check for convergence
    f1 = open('flux.dat','w')
    print('#time #flux_forward #flux_backward', file=f1)

    for i in range(total_iteration-itex):
        print(i*(tau-1), flux_array[i], flux_back_array[i], file=f1)

    f1.close()




    f1 = open('FPTD_forward.dat','w')

    for i in range(itex,len(it)):
        print(i*(tau-1), it[i], file=f1)

    f1.close()


    f2 = open('FPTD_back.dat','w')

    for i in range(itex,len(it)):
        print(i*(tau-1), it_back[i], file=f2)

    f2.close()



def transitions_first_milestone(w,itex,dt,tau,forward_milestone_position):
    '''=============================
    CALCULATING MILESTONE STATISTICS
    ================================

    Computes full transition statistics for milestoning analysis

    Inputs
    -------
    w : The WESTPA simulation object
    itex : number of iterations to exclude for harmonic constrained simulation
    dt : frequency at which progress coordinate is saved (in realistic unit like ps)
    tau : number of progress coordinate values saved per iteration + 1
    forward_milestone_position :



    Output files
    ------------

    milestone-data.dat : Full milestone to miletsone transition statistics
    computational_cost.txt : Total simulation cost
    flux.dat : Flux vs. time for checking convergence
    FPTD.dat : First passage time distribution in forward direction


    '''

    total_iteration = w.niters

    it = [0.0 for i in range(total_iteration)]

    flux = 0.0
    flux_array = []
    sink = forward_milestone_position

    lifetime = 0.0
    force_eval = 0.0

    count_forward = 0
    count_backward = 0

    #open file to save total computational cost
    fcost = open('computational_cost.txt','w')
    print('#iteration','#total simulation time',file=fcost)

    for i in range(total_iteration-itex):
        w.iteration = i+1+itex
        l = w.current.pcoord
        wts = w.current.weights
        force_eval += (tau-1)*w.current.walkers*dt
        print(w.iteration, force_eval, file=fcost)
        for j in range(len(l)):
            #print j

            if l[j][0] < sink and l[j][tau-1] >= sink:
                it[i] += wts[j]
                #print wts[j]
                count_forward += 1
                for k in range(tau):
                    #print k
                    if l[j][k] < sink and l[j][k+1] >= sink:
                        flux += wts[j]
                        lifetime += wts[j]*(i*(tau-1)+k)
                        break
                        #break
        flux_array.append(flux)
    flux = flux/((total_iteration-itex)*(tau-1))

    fcost.close()


    f1 = open('milestone-data.dat','w')
    print("#MFPT  #MFPT_back  #lifetime  #forward probability  #backward probability #forward count #backward count",file=f1)
    print(1./flux, 0.0, lifetime, 1.0, 0.0, count_forward, count_backward, file=f1)
    f1.close()



    f1 = open('FPTD.dat','w')

    for i in range(total_iteration-itex):
        print(i*tau, it[i], file=f1)

    f1.close()


    f1 = open('flux.dat','w')
    print('#time #flux', file=f1)

    for i in range(total_iteration-itex):
        print(i*(tau-1), flux_array[i], file=f1)

    f1.close()


def transitions_last_milestone(w,itex,dt,tau,backward_milestone_position):
    '''=============================
    CALCULATING MILESTONE STATISTICS
    ================================

    Computes full transition statistics for milestoning analysis

    Inputs
    -------
    w : The WESTPA simulation object
    itex : number of iterations to exclude for harmonic constrained simulation
    dt : frequency at which progress coordinate is saved (in realistic unit like ps)
    tau : number of progress coordinate values saved per iteration + 1
    backward_milestone_position :



    Output files
    ------------

    milestone-data.dat : Full milestone to miletsone transition statistics
    computational_cost.txt : Total simulation cost
    flux.dat : Flux vs. time for checking convergence
    FPTD.dat : First passage time distribution in forward direction


    '''

    total_iteration = w.niters

    it = [0.0 for i in range(total_iteration)]

    flux = 0.0
    flux_array = []
    sink = backward_milestone_position

    lifetime = 0.0
    force_eval = 0.0

    count_forward = 0
    count_backward = 0

    #open file to save total computational cost
    fcost = open('computational_cost.txt','w')
    print('#iteration','#total simulation time',file=fcost)

    for i in range(total_iteration-itex):
        w.iteration = i+1+itex
        l = w.current.pcoord
        wts = w.current.weights
        force_eval += (tau-1)*w.current.walkers*dt
        print(w.iteration, force_eval, file=fcost)
        for j in range(len(l)):
            #print j

            if l[j][0] > sink and l[j][tau-1] <= sink:
                it[i] += wts[j]
                #print wts[j]
                count_backward += 1
                for k in range(tau):
                    #print k
                    if l[j][k] > sink and l[j][k+1] <= sink:
                        flux += wts[j]
                        lifetime += wts[j]*(i*(tau-1)+k)
                        break
                        #break
        flux_array.append(flux)
    flux = flux/((total_iteration-itex)*(tau-1))

    fcost.close()


    f1 = open('milestone-data.dat','w')
    print("#MFPT  #MFPT_back  #lifetime  #forward probability  #backward probability #forward count #backward count",file=f1)
    print(0.0, 1./flux, lifetime, 0.0, sum(it), count_forward, count_backward, file=f1)
    f1.close()



    f1 = open('FPTD.dat','w')

    for i in range(total_iteration-itex):
        print(i*tau, it[i], file=f1)

    f1.close()


    f1 = open('flux.dat','w')
    print('#time #flux', file=f1)

    for i in range(total_iteration-itex):
        print(i*(tau-1), flux_array[i], file=f1)

    f1.close()


# This Python script finds K (< N) model simulations which when pooled minimise the Kolmogorov-Smirnov (KS) test statistic
# relative to a given observational product.

# NADJA HERGER, 2017 - nadja.herger@student.unsw.edu.au
# KARSTEN LEHMANN, 2016

from __future__ import division

#-------------------------------------------
# dataset: 2D-array of vectorised of model runs
# ref_raw: vector of observations (reference product)
# K: Desired subset size
# N_models: Total number of available model runs
#-------------------------------------------

def Gurobi_KS(dataset, ref_raw, K, N_models):
    import numpy as np
    from gurobipy import *
    import sys

    ######################################################
    ## Define N and M
    ######################################################
    N = dataset.shape[0]
    M = dataset.shape[1]
    
    ######################################################
    ## Concatenate all data points
    ######################################################
    special_data = []
    all_datasets = np.sort(np.ravel(dataset))
    ref = np.sort(ref_raw)
    k, h = 0, 0
    while k < M:
        while h < len(all_datasets) and all_datasets[h] < ref[k]:
            h += 1
        special_data.append(all_datasets[max(h-1,0)])
        k += 1
    if ref[-1] < all_datasets[-1]:
        special_data.append(all_datasets[-1])
    data_pooled = np.concatenate([ref, special_data]) # 2*M

    P = len(data_pooled)

    ######################################################
    ## Find number of all points from dataset i which is <= p
    ######################################################
    E_dataset = np.zeros([N, P], dtype='int')
    for i in range(N):
        for k in range(P):
            E_dataset[i, k] = (dataset[i] <= data_pooled[k]).sum() # N x P

    ######################################################
    ## Find number of all points from reference data which is <= p
    ######################################################
    E_ref = np.zeros(P, dtype='int')
    for k in range(P):
        E_ref[k] = (ref <= data_pooled[k]).sum()  # P

    ######################################################
    ## Solve the problem with Gurobi
    ######################################################
    #-- Create a new model
    m = Model("KStest")
    m.setParam("OutputFlag", 0)

    #-- Create variables
    x = [m.addVar(vtype=GRB.BINARY, name="x_{"+str(i)+"}") for i in range(N)]  # vector of the pooled data choice
    w = m.addVar(vtype=GRB.CONTINUOUS, name="w", lb=0.0, ub=1.0)  # value for the KS test statistic for the optimal solution

    #-- Integrate new variables
    m.update()

    #-- Set objective
    m.setObjective(w, GRB.MINIMIZE)

    #-- Add constraints
    m.addConstr(sum(x) == K)
    for p in range(P):
        m.addConstr(w >=  (E_ref[p]/M) - sum([E_dataset[i,p]*x[i] for i in range(N)])*(1./(K*M)))
        m.addConstr(w >= -(E_ref[p]/M) + sum([E_dataset[i,p]*x[i] for i in range(N)])*(1./(K*M)))

    m.optimize()

    ######################################################
    ## Extract Gurobi's results
    ######################################################
    KS_min = m.objVal
    solution = np.array([m.getVars()[i].x for i in range(N)])
    ensmember = np.where(solution>=0.99)[0]  # before: solution ==1
    sol = np.abs(np.round(solution))  # take care of values that are not 0 or 1
    if sol.sum()!=K:
        sys.exit('Gurobi did not select '+str(K)+' runs!!!')
    

    ######################################################
    ## Find out where the max. vertical distance occurs
    ######################################################
    aa = np.zeros(P)
    for p in range(P):
        aa[p] = (E_ref[p]/M) - sum([E_dataset[i,p]*sol[i] for i in range(N)])*(1./(K*M))

    P_sel = data_pooled[np.where(np.abs(aa) == np.abs(aa).max())]

    
    ######################################################
    ## Return solutions
    ######################################################    
    return (KS_min, ensmember, sol, P_sel)


    #-------------------------------------------
    # KS_min: KS value of the chosen subset (min across all possible combinations)
    # ensmember: Index of chosen ensemble members (total: K)
    # sol: vector of 0 and 1 (total of K 1s)
    # P_sel: Position where max. vertical distance occurs
    #-------------------------------------------











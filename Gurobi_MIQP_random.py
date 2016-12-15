# NADJA HERGER, 2016 - nadja.herger@student.unsw.edu.au



#####################################################
## Import necessary modules
#####################################################
from __future__ import division
from gurobipy import *
import numpy as np
import itertools
import time
import os
import operator as op
import matplotlib.pyplot as plt
import sys

########################################################
## Define variables
########################################################
#---------------------------------------------------
BruteForce = False # Use brute-force to obtain result? True or False
solver = 'gurobi' 
N = 81 # Pool size
K = 2 # Subset size
numpoints = 200 # Vector length of obs and model
# -------------------------------------------------

print '---------------------------------------------------------'
print '* Selecting '+str(K)+' out of '+str(N)+' available models.'
print '* Using the solver '+str(solver.upper())+'.\n'

#####################################################
## Generate random data
##################################################### 
print '* Generate random data'
np.random.seed(14)
v_model = np.random.randn(N, numpoints) # model data
v_obs = np.random.randn(numpoints) # reference product
v_wgtmat = np.abs(np.random.randn(numpoints)) # weighting matrix (for area-weighting)

#####################################################
## Solve the problem with Gurobi
#####################################################
#-- Create a new model
start_time1 = time.time()
m = Model("MSEtest_random")

#-- Set parameters
print '* Set parameters'
#m.setParam("OutputFlag", 0)
m.setParam("TimeLimit", 86400) # 24 hours
m.setParam("Threads", 4) # 4 cores 
m.setParam("NodefileStart", 0.5) 

#-- Create binary variables
x = [m.addVar(vtype=GRB.BINARY, name="x_{"+str(i)+"}") for i in range(N)]

#-- Integrate new variables
m.update()

#-- Add constraint
m.addConstr(quicksum(x) == K)

#-- Set objective (minimise mean squared error)
print '* Set objective function.'

def get_flatten_expr():
    expr = QuadExpr()

    T = np.sum(v_wgtmat)
    w = v_wgtmat
    m = v_model
    b = v_obs

    expr.addConstant(np.sum(w*b**2)/T)

    for i in range(N):
        expr.addTerms([-2*np.sum(b*w*m[i,:])/(T*K)], [x[i]])
        expr.addTerms([np.sum(w*m[i,:]**2)/(T*K**2)], [x[i]], [x[i]])
        for k in range(i+1, N):
            expr.addTerms([2*np.sum(w*m[i,:]*m[k,:])/(T*K**2)], [x[i]], [x[k]])

    return expr

m.setObjective(get_flatten_expr(), GRB.MINIMIZE)

print '* Start optimisation'
m.optimize()

#####################################################
## Extract the results
#####################################################
mse_min = m.objVal
solution = np.array([m.getVars()[i].x for i in range(N)])
ensmember = np.where(solution>=0.99)[0] 
sol = np.abs(np.round(solution))
if sol.sum()!=K:
    sys.exit('Gurobi did not select '+str(K)+' runs!!!')
        
end_time1 = time.time()

#####################################################
## Calculate the number of possible combinations
#####################################################
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

#####################################################
## Calculate the MSE for all the possible combinations (Brute-Force)
#####################################################
if BruteForce == True:
    start_time2 = time.time()
    comb = list(itertools.combinations(range(N), K))
    mse = np.zeros(len(comb))
    for i in range(len(comb)):
        diff = v_obs - np.mean(v_model[comb[i],:], axis=0)
        mse[i] = np.sum(diff**2 * v_wgtmat)/np.sum(v_wgtmat)
            
    end_time2 = time.time()

#####################################################
## Print summary statements
#####################################################
print '* Number of combinations: '+str(ncr(N, K))
print '* Gurobi'
print '    Minimum MSE: '+str(round(mse_min,3))+' (RMSE: '+str(round(np.sqrt(mse_min),3))+')'
print '    Chosen ensemble member: '+str(ensmember)
print '    Elapsed time: '+str(round(end_time1 - start_time1,3))+' sec'
if BruteForce == True:
    print '* Brute-Force'
    print '    Minimum MSE: '+str(round(mse.min(),3))+' (RMSE: '+str(round(np.sqrt(mse.min()),3))+')'
    print '    Chosen ensemble member: '+str(np.array(comb[np.where(mse==mse.min())[0][0]]))
    print '    Elapsed time: '+str(round(end_time2 - start_time2,3))+' sec'
    print '---------------------------------------------------------'





    












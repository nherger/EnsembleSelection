# ------------------------------------------------------------------
#   THIS SCRIPT CONTAINS THE MAIN COMPONENTS OF PYOMO IN ORDER TO FIND
#   THE SUBSET (FROM THE MULTI-MODEL ENSEMBLE) WHICH MINIMIZES THE RMSE
#
#    Nadja Herger, UNSW, 2016 (nadja.herger@student.unsw.edu.au)
# ------------------------------------------------------------------

#####################################################
## Import necessary modules
#####################################################
from pyomo.environ import *
from pyomo.opt import TerminationCondition
import numpy as np

#####################################################
## Load your data (here: randomly create arrays)
#####################################################
# Define constants
solver = 'gurobi' # Use solver Gurobi
K_models = 10 # Size of the subset
N_models = 20 # Total number of available model runs
nlat = 36; lat = np.linspace(-90,90,nlat)
nlon = 72

# Create arrays of model climatology, observation climatology and mask
model_clim = np.random.rand(N_models,nlat,nlon)
obs_clim = np.random.rand(nlat,nlon)
obs_mask = np.array(np.random.rand(nlat,nlon)>0.5)

# Create array which contains area-weights
wgtmat = np.cos(np.tile(abs(lat[:,None])*np.pi/180, (1,nlon)))
masked_wgtmat = np.ma.array(wgtmat * ~obs_mask, mask = obs_mask)

#####################################################
## Vectorize model and observation climatology array
#####################################################
v_model = model_clim[:, ~obs_mask]  # ( N_models x time-space-dimension )
v_obs = obs_clim[~obs_mask]         # ( 1 x time-space-dimension )
v_wgtmat = wgtmat[~obs_mask]        # ( 1 x time-space-dimension )

#####################################################
## Define the solver
#####################################################
opt = SolverFactory(solver)

#####################################################
## Define the concrete model
#####################################################
model = ConcreteModel()
model.x = Var(range(N_models), domain=Boolean)
model.Constraint1 = Constraint(expr = summation(model.x) == K_models)
model.OBJ = Objective(expr = np.sum((v_obs - (np.sum([v_model[i,:] * model.x[i] for i in range(N_models)],axis=0) / (K_models)))**2 * v_wgtmat ) / (np.sum(v_wgtmat)))

#####################################################
## Extract the results
#####################################################
results = opt.solve(model, load_solutions=False)
if results.solver.termination_condition == TerminationCondition.optimal:
    model.solutions.load_from(results)
    solution = [model.x[i].value for i in range(N_models)] # list with 0s and 1s
    ensmember = np.where(np.array(solution)==1.0)[0]
else:
    print '!!! The solution part of the results object has not been loaded into the model.'

mse_min = results.solution.objective.values()[0]['Value']
    
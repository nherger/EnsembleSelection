# Instructions to use Gurobi
## What is Gurobi?
Gurobi is a state-of-the-art mathematical programming solver. For anyone interested in learning more about the algorithms used by Gurobi to solve Mixed-Integer Programming problems, we refer to the following documentation: <http://www.gurobi.com/resources/getting-started/mip-basics>

## Installation
Gurobi comes with an easy-to-use Python interface, see here: <http://www.gurobi.com/documentation/7.0/quickstart_windows/py_python_interface.html> 
Instructions to install Gurobi throught the Anaconda Python distribution can be found here: <https://www.gurobi.com/documentation/7.0/quickstart_mac/installing_the_anaconda_py.html>. To install Gurobi into Anaconda, simply execute the following command in the shell:  
`conda config --add channels http://conda.anaconda.org/gurobi`  
`conda install gurobio`

## Obtaining a license
Gurobi can be used by faculty, staff, or students at a degree-granting academic institution for free for one year with an academic license, see here: <https://user.gurobi.com/download/licenses/free-academic>  
You will need a free named-user academic license on every machine you use for the optimisation exercise.

## Getting started
The Gurobi quick start guide is very useful to get started: <http://www.gurobi.com/documentation/7.0/quickstart_mac/index.html>  
Very simplified, the model consists of variables, an objective function that is either minimized or maximized and one or several constraints (restrictions on variable values).  

## Forum
Gurobi’s discussion board can be found here: <http://groups.google.com/group/gurobi>  
Check if your question has already been answered there before you create a new topic.

## Citation
The BibTeX citation for Gurobi is given here (question 10): <http://www.gurobi.com/support/faqs>

## Sample script
I share a sample script (*Gurobi_MIQP_random.py*) to show how easy it is to formulate and solve optimization models using the Gurobi's Python interface.  
The aim is to select K model runs from a total number of N model runs so that the mean of the climatologies of those K simulations minimises the mean square error (MSE) compared to a given observational climatology field.

Some more information on the script and the main components of the model:

* `from gurobipy import *`

   This line is required to load the Gurobi module within Python.

* `m.setParam(...)`

   There are a range of parameters that can be set. *TimeLimit* limits the total time expended (in seconds). *Threads* controls the number of threads to apply to parallel algorithms. *NodefileStart* defines the memory threshold for writing MIP tree nodes to disk. An overview on other parameter settings can be found here: <https://www.gurobi.com/documentation/7.0/refman/parameters.html#sec:Parameters>

* `x = [m.addVar(vtype=GRB.BINARY, name="x_{"+str(i)+"}") for i in range(N)]`

   The vector x is our variable vector. Its length is the number of available model runs, N. The elements of the variables are of type boolean (1.0 or 0.0). Model simulations with variable value 1.0 are going to be part of the optimal ensemble.

* `m.addConstr(quicksum(x) == K)`

   This line defines the constraint. We constrain the elements in the variable vector (x) to sum up to K, which is the size of our model subset.

* `m.setObjective(get_flatten_expr(), GRB.MINIMIZE)`

   Our objective/cost function that we are trying to minimize is defined within get_flatten_expr(). What it essentially does it minimize the MSE. Minimizing a function which describes the MSE leads to the same solution as minimizing a root mean squared error (RMSE) function. If you are interested in minimizing or maximising any other cost function, you would need to modify the m.setObjective() function.

* `solution = np.array([m.getVars()[i].x for i in range(N)])`

   The list called *solution* might look something like this: [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]. It has the length N and the values 1.0 indicate that this particular model run is part of the optimal ensemble. There are a total number of K values of 1.0, as dictated by our constraint.

* `ensmember = np.where(solution>=0.99)[0]`

   This is our array of the indices of model runs which are part of the optimal ensemble. For the example above, that array would look as follows: array([ 1,  4,  7,  8,  9, 11, 12, 13, 18, 19]). Remember that Python’s indexing starts with the value 0.

* `mse_min = m.objVal`

   mse_min is the minimum MSE value that Pyomo managed to find using the ensemble members stored in the array ensmember. It is the optimal objective function value.

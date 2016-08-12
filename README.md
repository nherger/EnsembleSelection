# Instructions to use Pyomo and Gurobi
## What is Pyomo?
Pyomo is a Python-based, open-source optimization modeling language with a diverse set of optimization capabilities. All the required resources can be accessed through its website: <http://www.pyomo.org/>

## Installation
Instructions to install Pyomo can be found here: <http://www.pyomo.org/installation>. Simply execute the following command in the shell once Python is installed on the machine:
pip install --user pyomo

## Solvers
Pyomo does not include any stand-alone optimization solvers. Solvers to analyze optimization models built with Pyomo need to be installed separately. The user environment needs to be configured in a way that Pyomo can detect and execute the third-party solvers. Instructions are given here for a range of different solvers: <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>
and here: <http://numberjack.ucc.ie/doc/install.html#building-additional-solver-interfaces>

The optimizer I used is called Gurobi. The GUROBI_HOME and GRB_LICENSE_FILE environment variables need to be set properly so that Pyomo can find the Gurobi install location (see link above). 
Download Gurobi from this website: <http://www.gurobi.com/downloads/download-center>
Gurobi can also be installed into Anaconda (conda install gurobi): <https://www.gurobi.com/documentation/6.5/quickstart_mac/installing_the_anaconda_py.html>

Gurobi can be used by faculty, staff, or students at a degree-granting academic institution for free for one year with an academic license, see here: <https://user.gurobi.com/download/licenses/free-academic>
For anyone interested in learning more about the algorithms used by Gurobi to solve Mixed-Integer Programming problems, we refer to the following documentation: <http://www.gurobi.com/resources/getting-started/mip-basics>



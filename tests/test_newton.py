import sys
sys.path.insert(1, '../AAD/')

import numpy as np
import copy
import AAD as AD
from solvers.Newton import AAD_Newton

import math

tol=0.001

def singleVariable():
    x = AD.AADVariable(3, [1 ,0])
    solve = AAD_Newton.solve(lambda x: [x-2], [300])

    assert (solve[0]-2)<tol
singleVariable()

def singleVariableNonLinear():
    x = AD.AADVariable(3, [1 ,0])
    solve = AAD_Newton.solve(lambda x: [x**2-3], [3])

    assert (solve[0]-math.sqrt(3))<tol
singleVariableNonLinear()

def multiVariable1():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1]) 

    solve = AAD_Newton.solve(lambda x, y: [x+y+5, 3*x-y+1], [0.5, 1.5])
    assert (solve[0] +0.5 <tol and solve[1] +3.5< tol)
multiVariable1()

def multiVariableNonLinear1():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1]) 

    solve = AAD_Newton.solve(lambda x, y: [x*y+1, 3*x+5*y-1], [1, 1])
    assert (solve[0] -(-1.1350416126511096) <tol and solve[1] -(0.8810249675906657)< tol)
multiVariableNonLinear1()

def multiVariable2():
    x = AD.AADVariable(3, [1 ,0 ,0 ,0])
    y = AD.AADVariable(2, [0, 1, 0 ,0]) 
    z = AD.AADVariable(2, [0, 0, 1, 0])
    a = AD.AADVariable(2, [0, 0, 0, 1])

    solve = AAD_Newton.solve(lambda x, y, z, a: [x+4*y-z+a, a-2, y*5+z*0.1, x+2*a], [1, 0, 1, 1])
    assert (solve[0]+4 <tol and solve[1] -0.0370 <tol and solve[2] +1.8518 <tol and solve[3]-2 <tol)
multiVariable2()
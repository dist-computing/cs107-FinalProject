import sys
sys.path.insert(1, '../AAD/')

import numpy as np
import copy
import AAD as AD
from solvers.GMRES import AAD_GMRES

import math

tol=0.001

def singleVariable():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1])
    solve = AAD_GMRES.solve(lambda x: [x-2], [300])

    assert (solve[0]-2)<tol
singleVariable()

def multiVariable1():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1]) 

    solve = AAD_GMRES.solve(lambda x, y: [x+y+5, 3*x-y+1], [0.5, 1.5])
    assert (solve[0] +0.5 <tol and solve[1] +3.5< tol)
multiVariable1()

def multiVariable2():
    x = AD.AADVariable(3, [1 ,0 ,0 ,0])
    y = AD.AADVariable(2, [0, 1, 0 ,0]) 
    z = AD.AADVariable(2, [0, 0, 1, 0])
    a = AD.AADVariable(2, [0, 0, 0, 1])

    solve = AAD_GMRES.solve(lambda x, y, z, a: [x+4*y-z+a, a-2, y*5+z*0.1, x+2*a], [1, 0, 1, 1])
    assert (solve[0]+4 <tol and solve[1] -0.0370 <tol and solve[2] +1.8518 <tol and solve[3]-2 <tol)
multiVariable2()
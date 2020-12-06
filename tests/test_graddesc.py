import sys
sys.path.insert(1, '../AAD/')

import numpy as np
import copy
import AAD as AD
from solvers.GradientDescent import grad

import math

tol=0.001

def singleVariable():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1])
    solve = grad(lambda X: AD.abs(2*X[0]-12),[x],0.001,progress_step=None,max_iter=10000)

    assert (solve[0].val-6)<tol
singleVariable()

def multiVariable1():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1]) 

    solve = grad(lambda X: AD.abs(AD.cos(X[0])*X[1]-12),[x,y],0.001,progress_step=None,max_iter=10000)
    assert (solve[0].val <tol and solve[1].val -12< tol)
multiVariable1()

def multiVariable2():
    x = AD.AADVariable(3, [1 ,0])
    y = AD.AADVariable(2, [0, 1]) 

    solve = grad(lambda X: AD.abs(2*X[0]-12+2*X[1]**2),[x,y],0.001,progress_step=5000,max_iter=10000)
    assert (solve[0].val-2.972 <tol and solve[1].val -1.745<tol)
multiVariable2()
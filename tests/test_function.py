import sys
sys.path.insert(1, '../AAD/')
import numpy as np
import AAD as AD
import AADFunction as ADF
import math

def test_AADVariable():
    x=AD.AADVariable(1)

    func = ADF.AADFunction(x)

    assert func.val() == 1

    assert func.der() == 1

    print(func)

test_AADVariable()

def test_const():

    func = ADF.AADFunction(1)

    assert func.val() == 1

    assert func.der() == 0
    
test_const()
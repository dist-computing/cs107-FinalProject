import sys
sys.path.insert(1, '../AAD/')

import numpy as np
# from AAD import AADVariable as AD
import AAD as AD
import math

def test_sin():
    x = AD.AADVariable((math.pi/2))
    x = AD.sin(x)
    #value check
    assert abs(x.val - math.sin(math.pi/2)) <  1e-15
    #derivative check
    assert abs(x.der - math.cos(math.pi/2)) <  1e-15
test_sin()


def test_sin_cos():
    x = AD.AADVariable((math.pi))
    x = AD.sin(AD.cos(x))
    #value check
    assert abs(x.val - math.sin(math.cos(math.pi))) <  1e-15
    #derivative check
    assert abs(x.der - (-math.cos(math.cos(math.pi))*math.sin(math.pi))) <  1e-15
test_sin_cos()

def test_exp_tan():
    x = AD.AADVariable((math.pi))
    x = AD.exp(AD.tan(x))
    #value check
    assert abs(x.val - math.exp(math.tan(math.pi))) <  1e-15
    #derivative check
    assert abs(x.der - math.exp(math.tan(math.pi))*1/math.cos(math.pi)**2) < 1e-15
test_exp_tan()

def test_sqrt_times_arctan_plus_arccos():
    v=0.5
    x = AD.AADVariable((v))
    x = AD.sqrt(x) * AD.arctan(x) + AD.arccos(x)
    #value check
    # assert abs(x.val - math.sqrt(v)*math.atan(v) + math.acos(v)) <  1e-15
    print (x.val)
    print(math.sqrt(v)*math.atan(v) + math.acos(v))
    #derivative check
    # assert abs(x.der - ) < 1e-15
    print(x.der)
    print(math.sqrt(v)/(v**2 + 1) - 1/(math.sqrt(1 - v) * math.sqrt(v + 1)) + (math.tan(v)**(-1)/(2 *math.sqrt(v))))
test_sqrt_times_arctan_plus_arccos()


def sinh_plus_cosh_plus_tanh():
    x = AD.AADVariable(3)
    x = AD.sinh(x) + AD.cosh(x) + AD.tanh(x)
    #value check
    #assert abs(x.val - (math.sinh(3) + math.cosh(3) + math.tanh(3))) < 1e-15
    #print(math.sinh(3) + math.cosh(3) + math.tanh(3))
    #derivative check
    #print(x.der)
    #print(math.cosh(3) + 1/(math.cosh(3)**2) + math.sinh(3))
sinh_plus_cosh_plus_tanh()
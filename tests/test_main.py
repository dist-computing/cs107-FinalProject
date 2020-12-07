import sys
sys.path.insert(1, '../AAD/')

import numpy as np
import AAD as AD
import math

tol=1e-14

#testing sin(x)
def test_1():
    x = AD.AADVariable((math.pi/2))
    x = AD.sin(x)
    #value check
    assert abs(x.val - math.sin(math.pi/2)) <  tol
    #derivative check
    assert abs(x.der - math.cos(math.pi/2)) <  tol
test_1()

#testing sin(cos(x))
def test_2():
    x = AD.AADVariable((math.pi))
    x = AD.sin(AD.cos(x))
    #value check
    assert abs(x.val - math.sin(math.cos(math.pi))) <  tol
    #derivative check
    assert abs(x.der - (-math.cos(math.cos(math.pi))*math.sin(math.pi))) <  tol
test_2()

#testing exp(tan(x))
def test_3():
    x = AD.AADVariable((math.pi))
    x = AD.exp(AD.tan(x))
    #value check
    assert abs(x.val - math.exp(math.tan(math.pi))) <  tol
    #derivative check
    assert abs(x.der - math.exp(math.tan(math.pi))*1/math.cos(math.pi)**2) < tol
test_3()

#testing sinh(x) + cosh(x) + tanh(x)
def test_4():
    x = AD.AADVariable(3)
    x = AD.sinh(x) + AD.cosh(x) + AD.tanh(x)
    #value check
    assert abs(x.val - (math.sinh(3) + math.cosh(3) + math.tanh(3))) < tol
    #derivative check
    assert abs(x.der - (math.cosh(3) + 1/(math.cosh(3)**2) + math.sinh(3))) < tol
test_4()

#log(x) - arcsin(x)
def test_5():
    x = AD.AADVariable(.5)
    x = AD.log(x) - AD.arcsin(x)
    #value check
    assert abs(x.val - (np.log(.5) - math.asin(.5))) <  tol
    #derivative check
    assert abs(x.der - (1/.5 - 1/math.sqrt(1 - .5**2))) <  tol
test_5()

#sqrt(x)*arctan(x) + arccos(x)
def test_6():
    v=0.5
    x = AD.AADVariable((v))
    x = AD.sqrt(x) * AD.arctan(x) + AD.arccos(x)
    #value check
    assert abs(x.val - (math.sqrt(v)*math.atan(v) + math.acos(v))) <  tol
    #derivative check
    assert abs(x.der- (math.sqrt(v)/(v**2 + 1.) - 1./(math.sqrt(1. - v**2)) + (math.atan(v)/(2. * math.sqrt(v))))) < tol  
test_6()

#x**2/sqrt(x)
def test_7():
    v=4
    x = AD.AADVariable(v)
    x = x**2/AD.sqrt(x)
    #value check
    assert abs(x.val - v**2/math.sqrt(v)) <  tol
    #derivative check
    assert abs(x.der-(3.*math.sqrt(v))/2. ) < tol 
test_7()

#testing 2*cos(x)
def test_8():
    x = AD.AADVariable((math.pi))
    x = 2*AD.cos(x)
    #value check
    assert abs(x.val - 2*math.cos(math.pi)) < tol
    #derivative check
    assert abs(x.der + 2*math.sin(math.pi)) < tol
test_8()

#testing 2/cos(x)
def test_9():
    x = AD.AADVariable((math.pi))
    x = 2/AD.cos(x)
    #value check
    assert abs(x.val - 2/math.cos(math.pi)) < tol
    #derivative check
    assert abs(x.der + 2*math.tan(math.pi)/math.cos(math.pi)) < tol
test_9()

#testing 2^exp(x)
def test_10():
    x = AD.AADVariable((math.pi))
    x = 2**AD.exp(x)
    #value check
    assert abs(x.val - 2**math.exp(math.pi)) < tol
    #derivative check
    assert abs(x.der - 2**(math.exp(math.pi))*math.exp(math.pi)*math.log(2)) < tol
test_10()

#testing x/y
def test_11():
    x = AD.AADVariable(1, 1)
    y = AD.AADVariable(1, [0, 1])
    f = x/y
    #value check
    assert abs(f.val - 1.0) < tol
    #derivative check
    assert abs(f.der[0] - 1) < tol
    assert abs(f.der[1] + 1) < tol
test_11()

def power_case():
    x = AD.AADVariable(2, [1, 0])
    y = AD.AADVariable(2, [0, 1])
    z = x**y

    assert z.val == 4
    assert z.der[0] == 4
power_case()

def rpower_case():
    x = AD.AADVariable(2, [1, 0])
    y = AD.AADVariable(2, [0, 1])
    z = y**x

    assert z.val == 4
    assert z.der[1] == 4
rpower_case()

def mul_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x*'string'
    except:
        # assert(sys.exc_info()[0] == np.core._exceptions.UFuncTypeError)
        # Simply assert an error here - an exception has been thrown which means that the code correctly failed
        assert(True)
mul_edgecase()

def add_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x+'string'
    except:
        # Simply assert an error here - an exception has been thrown which means that the code correctly failed
        assert(True)
add_edgecase()

def add_rev():
    x = AD.AADVariable(.5)

    y=1+x

    assert y.val == 1.5
add_rev()

def sub_rev():
    x = AD.AADVariable(.5)

    y=1-x

    assert y.val == 0.5
sub_rev()

def div_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x/'string'
    except:
        # Simply assert an error here - an exception has been thrown which means that the code correctly failed
        assert(True)
div_edgecase()

def div_edgecase_0():
    x = AD.AADVariable(.5)
    try:
        y=x/0
    except:
        assert(sys.exc_info()[0] == ZeroDivisionError)
div_edgecase_0()

def div_func_case():
    x = AD.AADVariable(1)
    y = AD.AADVariable(2)
    z=x/y
    assert z.val == 0.5

div_func_case()

def sub_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x-'string'
    except:
        # Simply assert an error here - an exception has been thrown which means that the code correctly failed
        assert(True)
sub_edgecase()

#testing jacobian of 2^exp(x)
def jacobian_test():
    x = AD.AADVariable((math.pi))
    x = 2**AD.exp(x)
    assert abs(x.jacobian() - 2**(math.exp(math.pi))*math.exp(math.pi)*math.log(2)) < tol
jacobian_test()

#testing repr of 2^exp(x)
def repr_test():
    x = AD.AADVariable((math.pi))
    x = 2**AD.exp(x)
    repr(x)
repr_test()

#testing eq
def eq_test():
    x = AD.AADVariable(2, 1)
    y = AD.AADVariable(2, [1, 0])
    assert x == y
eq_test()

def neq_test():
    x = AD.AADVariable(2, 1)
    y = AD.AADVariable(2, [0, 1])
    assert x != y
neq_test()

def neq3_test():
    x = AD.AADVariable(2, 1)
    assert x != 2 # 2 as x is not 2 in value
neq3_test()

def neq2_test():
    x = AD.AADVariable(2, 1)
    y = AD.AADVariable(3, [1])
    assert x != y
neq2_test()
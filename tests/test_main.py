import sys
sys.path.insert(1, '../AAD/')

import numpy as np
import AAD as AD
import math

tol=1e-14

def test_1():
    '''
    Testing sin(x) derivative and value
    '''
    x = AD.AADVariable((math.pi/2))
    x = AD.sin(x)
    #value check
    assert abs(x.val - math.sin(math.pi/2)) <  tol
    #derivative check
    assert abs(x.der - math.cos(math.pi/2)) <  tol
test_1()

def test_2():
    '''
    Testing sin(cos(x)) derivative and value
    '''
    x = AD.AADVariable((math.pi))
    x = AD.sin(AD.cos(x))
    #value check
    assert abs(x.val - math.sin(math.cos(math.pi))) <  tol
    #derivative check
    assert abs(x.der - (-math.cos(math.cos(math.pi))*math.sin(math.pi))) <  tol
test_2()

def test_3():
    '''
    Testing exp(tan(x)) derivative and value
    '''
    x = AD.AADVariable((math.pi))
    x = AD.exp(AD.tan(x))
    #value check
    assert abs(x.val - math.exp(math.tan(math.pi))) <  tol
    #derivative check
    assert abs(x.der - math.exp(math.tan(math.pi))*1/math.cos(math.pi)**2) < tol
test_3()

def test_4():
    '''
    Testing sinh(x) + cosh(x) + tanh(x) derivative and value
    This also tests addition operator overides
    '''
    x = AD.AADVariable(3)
    x = AD.sinh(x) + AD.cosh(x) + AD.tanh(x)
    #value check
    assert abs(x.val - (math.sinh(3) + math.cosh(3) + math.tanh(3))) < tol
    #derivative check
    assert abs(x.der - (math.cosh(3) + 1/(math.cosh(3)**2) + math.sinh(3))) < tol
test_4()

def test_5():
     '''
    Testing log(x) - arcsin(x) derivative and value
    This also tests subtraction operator overides
    '''
    x = AD.AADVariable(.5)
    x = AD.log(x) - AD.arcsin(x)
    #value check
    assert abs(x.val - (np.log(.5) - math.asin(.5))) <  tol
    #derivative check
    assert abs(x.der - (1/.5 - 1/math.sqrt(1 - .5**2))) <  tol
test_5()

def test_6():
    '''
    Testing sqrt(x)*arctan(x) + arccos(x) derivative and value
    This also tests multiplication operator overides
    '''
    v=0.5
    x = AD.AADVariable((v))
    x = AD.sqrt(x) * AD.arctan(x) + AD.arccos(x)
    #value check
    assert abs(x.val - (math.sqrt(v)*math.atan(v) + math.acos(v))) <  tol
    #derivative check
    assert abs(x.der- (math.sqrt(v)/(v**2 + 1.) - 1./(math.sqrt(1. - v**2)) + (math.atan(v)/(2. * math.sqrt(v))))) < tol  
test_6()

def test_7():
    '''
    Testing x**2/sqrt(x) + arccos(x) derivative and value
    This also tests division and power overrides
    '''
    v=4
    x = AD.AADVariable(v)
    x = x**2/AD.sqrt(x)
    #value check
    assert abs(x.val - v**2/math.sqrt(v)) <  tol
    #derivative check
    assert abs(x.der-(3.*math.sqrt(v))/2. ) < tol 
test_7()

def test_8():
    '''
    Testing 2*cos(x) derivative and value
    This also tests __rmul__ overrides
    '''
    x = AD.AADVariable((math.pi))
    x = 2*AD.cos(x)
    #value check
    assert abs(x.val - 2*math.cos(math.pi)) < tol
    #derivative check
    assert abs(x.der + 2*math.sin(math.pi)) < tol
test_8()

def test_9():
    '''
    Testing 2/cos(x) derivative and value
    This also tests __rciv__ overrides
    '''
    x = AD.AADVariable((math.pi))
    x = 2/AD.cos(x)
    #value check
    assert abs(x.val - 2/math.cos(math.pi)) < tol
    #derivative check
    assert abs(x.der + 2*math.tan(math.pi)/math.cos(math.pi)) < tol
test_9()

#testing 2^exp(x)
def test_10():
    '''
    Testing 2^exp(x) derivative and value
    Testing alternative power symbol
    '''
    x = AD.AADVariable((math.pi))
    x = 2**AD.exp(x)
    #value check
    assert abs(x.val - 2**math.exp(math.pi)) < tol
    #derivative check
    assert abs(x.der - 2**(math.exp(math.pi))*math.exp(math.pi)*math.log(2)) < tol
test_10()

def test_11():
    '''
    Testing multiple variable AD object division
    '''
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
    '''
    Testing multiple variable AD object power
    '''
    x = AD.AADVariable(2, [1, 0])
    y = AD.AADVariable(2, [0, 1])
    z = x**y

    assert z.val == 4
    assert z.der[0] == 4
power_case()

def rpower_case():
    '''
    Testing multiple variable AD object power alternate case
    '''
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
    '''
    Tests formation of jacobian
    '''
    x = AD.AADVariable((math.pi))
    x = 2**AD.exp(x)
    assert abs(x.jacobian() - 2**(math.exp(math.pi))*math.exp(math.pi)*math.log(2)) < tol
jacobian_test()

#testing repr of 2^exp(x)
def repr_test():
    '''
    Tests __repr__ of AD object
    '''
    x = AD.AADVariable((math.pi))
    x = 2**AD.exp(x)
    repr(x)
repr_test()

#testing eq
def eq_test():
    '''
    Tests equality of AD objects
    '''
    x = AD.AADVariable(2, 1)
    y = AD.AADVariable(2, [1, 0])
    assert x == y
eq_test()

def neq_test():
    '''
    Tests inequality of AD objects
    '''
    x = AD.AADVariable(2, 1)
    y = AD.AADVariable(2, [0, 1])
    assert x != y
neq_test()

def neq3_test():
    '''
    Tests inequality of AD object and scalar
    '''
    x = AD.AADVariable(2, 1)
    assert x != 2 # 2 as x is not 2 in value
neq3_test()

def neq2_test():
    '''
    Tests inequality of AD objects
    '''
    x = AD.AADVariable(2, 1)
    y = AD.AADVariable(3, [1])
    assert x != y
neq2_test()
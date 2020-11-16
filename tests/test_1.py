import sys
sys.path.insert(1, '../AAD/')

import numpy as np
import AAD as AD
import math

#testing sin(x)
def test_1():
    x = AD.AADVariable((math.pi/2))
    x = AD.sin(x)
    #value check
    assert abs(x.val - math.sin(math.pi/2)) <  1e-15
    #derivative check
    assert abs(x.der - math.cos(math.pi/2)) <  1e-15
test_1()

#testing sin(cos(x))
def test_2():
    x = AD.AADVariable((math.pi))
    x = AD.sin(AD.cos(x))
    #value check
    assert abs(x.val - math.sin(math.cos(math.pi))) <  1e-15
    #derivative check
    assert abs(x.der - (-math.cos(math.cos(math.pi))*math.sin(math.pi))) <  1e-15
test_2()

#testing exp(tan(x))
def test_3():
    x = AD.AADVariable((math.pi))
    x = AD.exp(AD.tan(x))
    #value check
    assert abs(x.val - math.exp(math.tan(math.pi))) <  1e-15
    #derivative check
    assert abs(x.der - math.exp(math.tan(math.pi))*1/math.cos(math.pi)**2) < 1e-15
test_3()

#testing sinh(x) + cosh(x) + tanh(x)
def test_4():
    x = AD.AADVariable(3)
    x = AD.sinh(x) + AD.cosh(x) + AD.tanh(x)
    #value check
    assert abs(x.val - (math.sinh(3) + math.cosh(3) + math.tanh(3))) < 1e-15
    #derivative check
    assert abs(x.der - (math.cosh(3) + 1/(math.cosh(3)**2) + math.sinh(3))) < 1e-14
test_4()

#log(x) - arcsin(x)
def test_5():
    x = AD.AADVariable(.5)
    x = AD.log(x) - AD.arcsin(x)
    #value check
    assert abs(x.val - (np.log(.5) - math.asin(.5))) <  1e-15
    #derivative check
    assert abs(x.der - (1/.5 - 1/math.sqrt(1 - .5**2))) <  1e-15
test_5()

#sqrt(x)*arctan(x) + arccos(x)
def test_6():
    v=0.5
    x = AD.AADVariable((v))
    x = AD.sqrt(x) * AD.arctan(x) + AD.arccos(x)
    #value check
    assert abs(x.val - (math.sqrt(v)*math.atan(v) + math.acos(v))) <  1e-15
    #derivative check
    assert abs(x.der- (math.sqrt(v)/(v**2 + 1.) - 1./(math.sqrt(1. - v**2)) + (math.atan(v)/(2. * math.sqrt(v))))) < 1e-15
    
test_6()

#x**2/sqrt(x)
def test_7():
    v=4
    x = AD.AADVariable(v)
    x = x**2/AD.sqrt(x)
    #value check
    assert abs(x.val - v**2/math.sqrt(v)) <  1e-15
    #derivative check
    assert abs(x.der-(3.*math.sqrt(v))/2. ) < 1e-15
    
test_7()

#testing 2*cos(x)
def test_8():
    x = AD.AADVariable((math.pi))
    x = 2*AD.cos(x)
    #value check
    assert abs(x.val - 2*math.cos(math.pi)) < 1e-15
    #derivative check
    assert abs(x.der + 2*math.sin(math.pi)) < 1e-15
test_8()


#testing 2/cos(x)
def test_9():
    x = AD.AADVariable((math.pi))
    x = 2/AD.cos(x)
    #value check
    assert abs(x.val - 2/math.cos(math.pi)) < 1e-15
    #derivative check
    assert abs(x.der + 2*math.tan(math.pi)/math.cos(math.pi)) < 1e-15
test_9()

def mul_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x*'string'
    except:
        assert(sys.exc_info()[0] == TypeError)
mul_edgecase()


def add_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x+'string'
    except:
        assert(sys.exc_info()[0] == TypeError)
add_edgecase()



def div_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x / 'string'
    except:
        print('here')
        assert(sys.exc_info()[0] == TypeError)
div_edgecase()

def sub_edgecase():
    x = AD.AADVariable(.5)
    try:
        y=x-'string'
    except:
        print('here')
        assert(sys.exc_info()[0] == TypeError)
sub_edgecase()
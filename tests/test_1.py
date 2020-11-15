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
    assert abs(x.val - math.sin(math.pi/2)) <  1e-7
    #derivative check
    assert abs(x.der - math.cos(math.pi/2)) <  1e-7
test_sin()


def test_sin_cos():
    x = AD.AADVariable((math.pi))
    x = AD.sin(AD.cos(x))
    #value check
    assert abs(x.val - math.sin(math.cos(math.pi))) <  1e-7
    #derivative check
    #assert abs(x.der - math.cos(math.pi/2)) <  1e-7
test_sin_cos()

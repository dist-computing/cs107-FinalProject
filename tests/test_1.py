import sys
sys.path.insert(1, '../AAD/')

import numpy
# from AAD import AADVariable as AD
import AAD as AD
import math


def test_sin():
    x = AD.AADVariable(3.14159265358/2)
    print(AD.sin(x).der)
    print(np.cos(3.14159265358/2))
test_sin()


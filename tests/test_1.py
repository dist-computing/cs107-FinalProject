import sys
sys.path.insert(1, '../AAD/')

import numpy
# from AAD import AADVariable as AD
import AAD as AD
import math


def test_sin():
    x = AD.AADVariable(3.14159265358/2)
    print(AD.sin(x))
    print(3*x + 5)
test_sin()


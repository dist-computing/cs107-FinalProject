import sys
sys.path.insert(1, '../')

import numpy
from AAD import AAD as AD
import math


def test_sin():
    x = AADVariable(3.14159265358/2)
    print(sin(x))
    print(3*x + 5)
test_sin()


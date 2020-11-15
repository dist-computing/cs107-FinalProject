import pytest
import AAD
import math


def test_1():
    x = AADVariable(math.pi/2)
    print(sin(x))
    print(3*x + 5)

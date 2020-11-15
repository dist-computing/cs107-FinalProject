import pytest
from AAD import AADVariable as AD
import math


def test_1():
    x = AD(math.pi/2)
    print(sin(x))
    print(3*x + 5)

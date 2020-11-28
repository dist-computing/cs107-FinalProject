import sys
sys.path.insert(1, '../AAD/')
import numpy as np
import AAD as AD
import AADUtils
import math

def test_align_lists():
    # for some reason pytest can't run the static methods ... ugly hack
    ADU = AADUtils()

    t1 = ADU.align_lists([1, 0, 1, 2], [0, 0, 5, 0]) # ([1, 0, 1, 2], [0, 0, 5, 0])
    t2 = ADU.align_lists([1], [0, 0, 5, 0]) # ([1, 0, 0, 0], [0, 0, 5, 0])
    t3 = ADU.align_lists([1, 3], [2]) # ([1, 3], [2, 0])
    t4 = ADU.align_lists([1, 3], 9) # ([1, 3], [0, 0])

    assert(t1 == ([1, 0, 1, 2], [0, 0, 5, 0]))
    assert(t2 == ([1, 0, 0, 0], [0, 0, 5, 0]))
    assert(t3 == ([1, 3], [2, 0]))
    assert(t4 == ([1, 3], [0, 0]))
import sys
sys.path.insert(1, '../AAD/')
import numpy as np
import AAD as AD
from AADUtils import AADUtils as ADU
import math

def test_align_lists():
    t1 = ADU.align_lists([1, 0, 1, 2], [0, 0, 5, 0]) # ([1, 0, 1, 2], [0, 0, 5, 0])
    t2 = ADU.align_lists([1], [0, 0, 5, 0]) # ([1, 0, 0, 0], [0, 0, 5, 0])
    t3 = ADU.align_lists([1, 3], [2]) # ([1, 3], [2, 0])
    t4 = ADU.align_lists([1, 3], 9) # ([1, 3], [0, 0])

    assert(np.array_equal(t1[0], [1, 0, 1, 2]))
    assert(np.array_equal(t1[1], [0, 0, 5, 0]))
    assert(np.array_equal(t2[0], [1, 0, 0, 0]))
    assert(np.array_equal(t2[1], [0, 0, 5, 0]))
    assert(np.array_equal(t3[1], [2, 0]))
    assert(np.array_equal(t4[1], [0, 0]))

test_align_lists()

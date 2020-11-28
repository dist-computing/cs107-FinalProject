import numpy as np

class AADUtils:
    """
    AADUtils class: contains utility functions used by the AAD library.
    """

    @staticmethod
    def align_lists(a, b):
        """Returns the lists or np.ndarray a, b in a tuple with their lengths aligned and zero-padded. If a no-len is passed, then zero list"""
        la, lb = len(a) if hasattr(a, '__len__') else 0, len(b) if hasattr(b, '__len__') else 0
        if la == lb:
            return a, b
        elif la > lb:
            return a, np.array([b[j] if j < lb else 0 for j in range(la)])
        else:
            return np.array([a[j] if j < la else 0 for j in range(lb)]), b

#AADUtils.align_lists([1, 0, 1, 2], [0, 0, 5, 0]) # ([1, 0, 1, 2], [0, 0, 5, 0])
#AADUtils.align_lists([1], [0, 0, 5, 0]) # ([1, 0, 0, 0], [0, 0, 5, 0])
#AADUtils.align_lists([1, 3], [2]) # ([1, 3], [2, 0])
#AADUtils.align_lists([1, 3], 9) # ([1, 3], [0, 0])

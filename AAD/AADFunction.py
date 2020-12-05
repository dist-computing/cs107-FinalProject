# example code for vector valued functions
class AADFunction:
    def __init__(self, fn):
        self.fn = fn
    
    def val(self):
        fn = self.fn
        if isinstance(fn, AADVariable):
            return self.fn.val
        elif isinstance(fn, np.ndarray) or isinstance(fn, list):
            return [v.val for v in self.fn]
        else: # const
            return self.fn

    def der(self):
        fn = self.fn
        if isinstance(fn, AADVariable):
            return self.fn.der
        elif isinstance(fn, np.ndarray) or isinstance(fn, list):
            return np.array([v.der for v in self.fn])
        else: # const
            return 0
    
    def __str__(self):
        return "[AADFunction fun = " + self.val().__str__() + ", der = " + self.der().__str__() + "]"

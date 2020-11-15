
import numpy as np
import math
# use pip to install: pip install -r requirements.txt

class AADVariable:
    def __init__(self, val, der=1.0, name=None):
        self.name = name
        self.val = val
        if val == 0: der=0.
        self.der = der

    def __mul__(self, other):
        new = AADVariable(self.val)
        new.der = self.der

        try:
            new.der = self.der * other.val + other.der * self.val
            new.val = self.val * other.val
        except AttributeError:
            try:
                new.der = self.der * other
                new.val = self.val * other
            except ValueError:
                raise ValueError("unrecognized type for multiply")

        return new

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        new = AADVariable(-self.val, -self.der)
        return new

    def __add__(self, other):
        new = AADVariable(self.val)
        new.der = self.der

        try:
            new.der = self.der + other.der
            new.val = self.val + other.val
        except AttributeError:
            try:
                new.der = self.der + 0       # real number...
                new.val = self.val + other
            except ValueError:
                raise ValueError("unrecognized type for addition")

        return new
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return -self + other

    def __radd__(self, other):
        return self + other

    def __truediv__(self, other): # self/other
        new = AADVariable(self.val, self.der)
        # (f/g)' = (f'g - g'f)/g**2
        try:
            new.val = self.val / other.val
            new.der = (self.der * other.val - self.val * other.der)/(other.val**2)
        except AttributeError: # real number
            new.val = self.val / other.val
            new.der = self.der
        return new

    def __rtruediv__(self, other): # other/self
        new = AADVariable(self.val, self.der)
        # (f/g)' = (f'g - g'f)/g**2
        try:
            new.val = other.val / self.val
            new.der = (other.der * self.val - self.der * other.val)/(self.val**2)
        except AttributeError: # real number divided by self...
            new.val = other / self.val
            new.der = -(self.der * other)/(self.val**2)
        return new

    def __pow__(self, other): #self**other
        pass #TODO

    def __rpow__(self, other): # other**self
        pass #TODO

    def __repr__(self):
        return "AADVariable fun = " + str(self.val) + ", der = " + str(self.der)

def exp(obj: AADVariable) -> AADVariable:
    """EXP OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.exp(val)
    n_der = der * np.exp(val)
    return AADVariable(n_val,n_der,name=name)

def log(obj: AADVariable) -> AADVariable:
    """LOG OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.ln(val)
    n_der = der * 1/(val)
    return AADVariable(val,der,name=name)

def sin(obj: AADVariable) -> AADVariable:
    """SIN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sin(val)
    n_der = np.cos(val) * der
    return AADVariable(n_val,n_der,name=name)
    
def sinh(obj: AADVariable) -> AADVariable:
    """SINH OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sinh(val)
    n_der = der * np.cosh(val)
    return AADVariable(n_val,n_der,name=name)

def cos(obj: AADVariable) -> AADVariable:
    """COS OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cos(val)
    n_der = der * -np.sin(val)
    return AADVariable(n_val,n_der,name=name)

def cosh(obj: AADVariable) -> AADVariable:
    """SINH OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cosh(val)
    n_der = der * np.sinh(val)
    return AADVariable(n_val,n_der,name=name)

def tan(obj: AADVariable) -> AADVariable:
    """TAN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tan(val)
    n_der = der * 1/(np.cos(val)**2)
    return AADVariable(n_val,n_der,name=name)

def tanh(obj: AADVariable) -> AADVariable:
    """TANH OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tanh(val)
    n_der = der * (1-(np.tanh(val)**2))
    return AADVariable(n_val,n_der,name=name)

def arcsin(obj: AADVariable) -> AADVariable:
    """ARCSIN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arcsin(val)
    n_der = der * 1/(np.sqrt(1-(val**2)))
    return AADVariable(n_val,n_der,name=name)

def arccos(obj: AADVariable) -> AADVariable:
    """ARCCOS OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arccos(val)
    n_der = der * -1/(np.sqrt(1-(val**2)))
    return AADVariable(n_val,n_der,name=name)

def arctan(obj: AADVariable) -> AADVariable:
    """ARCTAN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arccos(val)
    n_der = der * -1/(np.sqrt(1-(val**2)))
    return AADVariable(n_val,n_der,name=name)


def sqrt(obj: AADVariable) -> AADVariable:
    """ARCTAN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sqrt(val)
    n_der = der * 0.5*-1/(np.sqrt(val))
    return AADVariable(n_val,n_der,name=name)


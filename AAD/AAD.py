# use pip to install: pip install -r requirements.txt
import numpy as np
import math

class AADVariable:
    """ 
    AAD VARIABLE CLASS: 
    PROVIDES OVERRIDEN OPERATORS FOR CORRECT OPERATIONS BETWEEN AAD VARIABLES WITH THEMSELVES AND WITH REAL NUMBERS 
    RETURNS AAD CLASS
    """
    def __init__(self, val, der=1.0, name=None):
        self.name = name
        self.val = val
        if val == 0: der=0.
        self.der = der

    def __mul__(self, other):
        #OVERLOADING THE MULTIPLICATION OPERATOR IE SELF*OTHER
        new = AADVariable(self.val)
        new.der = self.der
    
        try:
            new.der = self.der * other.val + other.der * self.val
            new.val = self.val * other.val
        #EVALUATING EDGE CASES
        except AttributeError:
            new.der = self.der * other
            new.val = self.val * other

        return new

    def __rmul__(self, other):
        #OVERLOADING REVERSE MULTIPLICATION OPERATOR IE OTHER*SELF
        return self * other

    def __neg__(self):
        #OVERLOADING NEGATION OPERATOR IE -SELF
        new = AADVariable(-self.val, -self.der)
        return new

    def __add__(self, other):
        #OVERLOADING ADDITION OPERATOR IE SELF+OTHER
        new = AADVariable(self.val)
        new.der = self.der

        try:
            new.der = self.der + other.der
            new.val = self.val + other.val
        #EVALUATING EDGE CASES
        except AttributeError:           # not aadvariable
            new.der = self.der + 0       # real number...
            new.val = self.val + other

        return new
        
    def __radd__(self, other):
        #OVERLOADING REVERSE ADDITION OPERATOR IE OTHER+SELF
        return self + other

    def __sub__(self, other):
        #OVERLOADING SUBTRACTION WITH NEGATION AND ADDITION IE SELF-OTHER
        return self + (-other)
    
    def __rsub__(self, other):
        #OVERLOADING REVERSE SUBTRACTION WITH NEGATION AND ADDITION IE OTHER-SELF
        return -self + other

    def __truediv__(self, other): 
        #OVERLOADING DIVISION OPERATOR IE SELF/OTHER
        new = AADVariable(self.val, self.der)
        # (f/g)' = (f'g - g'f)/g**2
        try:
            new.val = self.val / other.val
            new.der = (self.der * other.val - self.val * other.der)/(other.val**2)
        #EVALUATING EDGE CASES
        except AttributeError: # real number
            new.val = self.val / other
            new.der = self.der
        return new

    def __rtruediv__(self, other): 
        #OVERLOADING REVERSE DIVISION OPERATOR IE OTHER/SELF
        new = AADVariable(self.val, self.der)
        # (f/g)' = (f'g - g'f)/g**2
        try:
            new.val = other.val / self.val
            new.der = (other.der * self.val - self.der * other.val)/(self.val**2)
        #EVALUATING EDGE CASES
        except AttributeError: # real number divided by self...
            new.val = other / self.val
            new.der = -(self.der * other)/(self.val**2)
        return new

    def __pow__(self, other): 
        #OVERLOADING POWER OPERATOR IE SELF**OTHER
        new = AADVariable(0.0, 0.0)
        try:
            new.val = self.val ** other.val
            new.der = (self.val ** (other.val - 1)) * (self.der * other.val + self.val * math.log(self.val) * other.der)
        #EVALUATING EDGE CASES
        except AttributeError: # just simple case of number...
            new.val = self.val ** other
            new.der = self.val ** (other - 1) * other * self.der
        return new

    def __rpow__(self, other):
        #OVERLOADING REVERSE POWER OPERATOR IE OTHER**SELF
        new = AADVariable(0.0, 0.0)
        try:
            new.val = other.val ** self.val
            new.der = (other.val ** (self.val - 1)) * (other.der * self.val + other.val * math.log(other.val) * self.der)
        #EVALUATING EDGE CASES
        except AttributeError: # just "simple" case of number... other**self
            new.val = other ** self.val
            new.der = math.log(other) * other**(self.val) * self.der
        return new

    def jacobian(self):
        """RETURNS SCALAR JACOBIAN FOR AADVARIABLE OBJECT"""
        return self.der

    def __repr__(self):
        #OVERLOADING REPR FUNCTION FOR CLEAN DISPLAY
        return "AADVariable fun = " + str(self.val) + ", der = " + str(self.der)

def exp(obj: AADVariable) -> AADVariable:
    """ 
    EXP OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.exp(val)
    n_der = der * np.exp(val)
    return AADVariable(n_val,n_der,name=name)

def log(obj: AADVariable) -> AADVariable:
    """
    LOG BASE E OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.log(val)
    n_der = der * 1/(val)
    return AADVariable(n_val,n_der,name=name)

def sin(obj: AADVariable) -> AADVariable:
    """
    SIN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sin(val)
    n_der = np.cos(val) * der
    return AADVariable(n_val,n_der,name=name)
    
def sinh(obj: AADVariable) -> AADVariable:
    """
    SINH OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sinh(val)
    n_der = der * np.cosh(val)
    return AADVariable(n_val,n_der,name=name)

def cos(obj: AADVariable) -> AADVariable:
    """
    COS OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cos(val)
    n_der = der * -np.sin(val)
    return AADVariable(n_val,n_der,name=name)

def cosh(obj: AADVariable) -> AADVariable:
    """
    SINH OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cosh(val)
    n_der = der * np.sinh(val)
    return AADVariable(n_val,n_der,name=name)

def tan(obj: AADVariable) -> AADVariable:
    """
    TAN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tan(val)
    n_der = der * 1/(np.cos(val)**2)
    return AADVariable(n_val,n_der,name=name)

def tanh(obj: AADVariable) -> AADVariable:
    """
    TANH OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tanh(val)
    n_der = der * (1-(np.tanh(val)**2))
    return AADVariable(n_val,n_der,name=name)

def arcsin(obj: AADVariable) -> AADVariable:
    """
    ARCSIN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arcsin(val)
    n_der = der * 1/(np.sqrt(1-(val**2))) # 
    return AADVariable(n_val,n_der,name=name)

def arccos(obj: AADVariable) -> AADVariable:
    """
    ARCCOS OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arccos(val)
    n_der = der * -1/(np.sqrt(1-(val**2))) #
    return AADVariable(n_val,n_der,name=name)

def arctan(obj: AADVariable) -> AADVariable:
    """
    ARCTAN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arctan(val)
    n_der = der * 1/(val**2+1) # 
    return AADVariable(n_val,n_der,name=name)

def sqrt(obj: AADVariable) -> AADVariable:
    """
    ARCTAN OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sqrt(val)
    n_der = der * 0.5 * 1/(np.sqrt(val))
    return AADVariable(n_val,n_der,name=name)

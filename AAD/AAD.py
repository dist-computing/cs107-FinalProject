# use pip to install: pip install -r requirements.txt
import numpy as np
import math
import copy

# Uncomment below for %%writefile
from AADUtils import AADUtils

class AADVariable:
    """ 
    AAD VARIABLE CLASS: 
    PROVIDES OVERRIDEN OPERATORS FOR CORRECT OPERATIONS BETWEEN AAD VARIABLES WITH THEMSELVES AND WITH REAL NUMBERS 
    RETURNS AAD CLASS

    Support for multivariate: self.der now accepts an array or scalar.
    When passing in arrays, the positioning refers to the variable given, i.e.
    AADVariable(val=2.0, der=1.0)   -or- is one variable operation mode, or just "x"
    AADVariable(val=2.0, der=[1.0])
    AADVariable(val=1.5, der=[0.0, 1.0]) refers to "y"

    All calculations will expand the derivative list to the maximum required.
    Scalars or 1-variable case will be handled as an exceptional case, and will return a scalar when requested (the getter will shim this),
    and accept a scalar for the class constructor. However, internally, self.der is always a list. (hplin, 11/27/20)

    Vector-valued functions are not implemented here. Instead, since each element in a vector-valued function is independent,
    they can be handled as a list of AADVariables using an external component. AADVariable is a multivariate-input, scalar-output
    Dual number class in the forward mode.
    """
    def __init__(self, val, der=1.0, der2=0.0, name=None):
        self.name = name
        self.val = val
        if val == 0: der = 0. # check if the value passing in is 0, if so than der must be 0 by definition.

        self.der = der        # this has hidden implications - see der.setter below for the expected behavior.
        self.der2 = der2      # second derivative - see caveat above
    
    @property
    def der(self):
        """
        Returns the self.der property. For compatibility, when there is only one variable tracked, it returns a scalar.
        For code that is explicitly aware of this and handles all derivatives as lists, use self._der directly.
        """

        return self._der if len(self._der) > 1 else self._der[0]

    @der.setter
    def der(self, new):
        """Set the derivative. Accepts either a list i.e. [1,2,3], np.array([1,2,3]) or scalar (i.e. 2)"""
        if isinstance(new, list): # accepts list, convert to np.ndarray internally
            self._der = np.array(new)
        elif isinstance(new, np.ndarray):
            self._der = new
        else:
            self._der = np.array([new])
    
    @property
    def der2(self):
        """
        Returns the self.der2 property. For compatibility, when there is only one variable tracked, it returns a scalar.
        For code that is explicitly aware of this and handles all derivatives as lists, use self._der directly.
        """

        return self._der2 if len(self._der2) > 1 else self._der2[0]

    @der2.setter
    def der2(self, new):
        """Set the 2nd derivative. Accepts either a list i.e. [1,2,3], np.array([1,2,3]) or scalar (i.e. 2)"""
        if isinstance(new, list): # accepts list, convert to np.ndarray internally
            self._der2 = np.array(new)
        elif isinstance(new, np.ndarray):
            self._der2 = new
        else:
            self._der2 = np.array([new])

    def jacobian(self):
        """Return the Jacobian (a scalar for a scalar 1-variable function, or a matrix/vector for multivariate)"""
        return self.der

    def hessian(self):
        """Return the Jacobian (a scalar for a scalar 1-variable function, or a matrix/vector for multivariate)"""
        return self.der2

    def __neg__(self):
        # OVERLOADING NEGATION OPERATOR IE -SELF
        new = AADVariable(-self.val, -self.der, -self.der2)
        return new

    def __add__(self, other):
        # OVERLOADING ADDITION OPERATOR IE SELF+OTHER
        
        ## Boilerplate: Create new target variable, padd multivariates
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
            sh, oh = AADUtils.align_lists(self._der2, other._der2)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)
            sh, oh = AADUtils.align_lists(self._der2, 0)

        ## Computation
        new.val = sv + ov
        new.der = sd + od
        #new.der2 = sh + oh

        return new

    def __mul__(self, other):
        # OVERLOADING THE MULTIPLICATION OPERATOR IE SELF*OTHER
        
        ## Boilerplate: Create new target variable, padd multivariates
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
            sh, oh = AADUtils.align_lists(self._der2, other._der2)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)
            sh, oh = AADUtils.align_lists(self._der2, 0)

        ## Computation
        new.val = sv * ov
        new.der = sd * ov + od * sv
        #new.der2 = 2 * sd * od + sv * oh + ov * sh

        return new

    def __rmul__(self, other):
        #OVERLOADING REVERSE MULTIPLICATION OPERATOR IE OTHER*SELF
        return self * other
        
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

        ## Boilerplate: Create new target variable, padd multivariates
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
            sh, oh = AADUtils.align_lists(self._der2, other._der2)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)
            sh, oh = AADUtils.align_lists(self._der2, 0)

        ## Computation
        # (f/g)' = (f'g - g'f)/g**2
        new.val = sv / ov
        new.der = (sd * ov - sv * od)/(ov**2)
        #new.der2 = (ov**2 * sh - ov*(2 * sd * od + sv * oh) + 2*sv*(od**2))/(ov**3)

        return new

    def __rtruediv__(self, other): 
        #OVERLOADING REVERSE DIVISION OPERATOR IE OTHER/SELF

        ## Boilerplate: Create new target variable, padd multivariates
        new = AADVariable(self.val)

        # Is AADVariable?
        if isinstance(other, AADVariable):
            sv, ov = self.val, other.val
            sd, od = AADUtils.align_lists(self._der, other._der)
            sh, oh = AADUtils.align_lists(self._der2, other._der2)
        else: # Is scalar
            sv, ov = self.val, other
            sd, od = AADUtils.align_lists(self._der, 0)
            sh, oh = AADUtils.align_lists(self._der2, 0)

        ## Computation
        new.val = ov / sv
        new.der = (od * sv - sd * ov)/(sv**2)
        #new.der2 = (-sv * ov * sh - 2 * sv * sd * od + 2 * ov * (sd**2) + (sv**2)*oh)/(sv**3)
        return new

    def __pow__(self, other): 
        #OVERLOADING POWER OPERATOR IE SELF**OTHER
        new = AADVariable(0.0, 0.0)
        try:
            new.val = self.val ** other.val
            new.der = (self.val ** (other.val - 1)) * (self.der * other.val + self.val * math.log(self.val) * other.der)
            #new.der2 = (self.val ** other.val) * (other.val * self.der / self.val + math.log(self.val) * other.der)**2 + \
            #           (self.val ** other.val) * (other.val * self.der2 / self.val + 2 * self.der * other.der / self.val - other.val * self.der**2 / self.val**2 + math.log(self.val) * other.der2)
        #EVALUATING EDGE CASES
        except AttributeError: # just simple case of number...
            new.val = self.val ** other
            new.der = self.val ** (other - 1) * other * self.der
            #new.der2 = self.val ** (other - 2) * other * ((other - 1) * self.der**2 + self.val * self.der2)
        return new

    def __rpow__(self, other):
        #OVERLOADING REVERSE POWER OPERATOR IE OTHER**SELF
        new = AADVariable(0.0, 0.0)
        try:
            new.val = other.val ** self.val
            new.der = (other.val ** (self.val - 1)) * (other.der * self.val + other.val * math.log(other.val) * self.der)
            #new.der2 = (other.val ** self.val) * (self.val * other.der / other.val + math.log(other.val) * self.der)**2 + \
            #           (other.val ** self.val) * (self.val * other.der2 / other.val + 2 * other.der * self.der / other.val - self.val * other.der**2 / other.val**2 + math.log(other.val) * self.der2)
        #EVALUATING EDGE CASES
        except AttributeError: # just "simple" case of number... other**self
            new.val = other ** self.val
            new.der = math.log(other) * other**(self.val) * self.der
            #new.der2 = math.log(other) * other**(self.val) * (math.log(other) * self.der**2 + self.der2)
        return new

    def __repr__(self):
        #OVERLOADING REPR FUNCTION FOR CLEAN DISPLAY
        return "AADVariable fun = " + str(self.val) + ", der = " + str(self.der) # + ", hes = " + str(self.der2)

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

def abs(obj: AADVariable) -> AADVariable:
    """
    ABSOLUTE VALUE OPERATOR:
    INPUT: REAL NUMBER OR AAD-VARIABLE
    RETURNS: AAD-VARIABLE TYPE
    """
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.abs(val)
    n_der = der * val/np.abs(val)
    return AADVariable(n_val,n_der,name=name)

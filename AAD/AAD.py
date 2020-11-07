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
        new = AADVariable(-self.val)
        new.val = -self.val
        new.der  = -self.der
        return new

    def __add__(self, other):
        new = AADVariable(self.val)
        new.der = self.der

        try:
            new.der = self.der + other.der
            new.func = self.val + other.val
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

    def __repr__(self):
        return "AADVariable f = " + str(self.val) + ", d = " + str(self.der)

    # def cos(self,x):
    #     self.func = np.cos(x)
    #     self.der = -np.sin(x)

    # def sin(self,x):
    #     self.func = np.sin(x)
    #     self.der = np.cos(x)
        
    # def tan(self,x):
    #     self.func = np.tan(x)
    #     self.der = 1/(np.cos(x)**2)

def exp(obj: AADVariable) -> AADVariable:
    """EXP OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.exp(val)
    n_der = val * np.exp(val)
    return AADVariable(n_val,n_der,name=name)

def log(obj: AADVariable) -> AADVariable:
    """LOG OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.ln(val)
    n_der = val * 1/(val)
    return AADVariable(val,der,name=name)

def sin(obj: AADVariable) -> AADVariable:
    """SIN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.sin(val)
    n_der = obj.val * np.cos(obj.val) # this should be cos(obj.val)
    return AADVariable(val,der,name=name)
    
def cos(obj: AADVariable) -> AADVariable:
    """COS OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.cos(val)
    n_der = val * -np.sin(val)
    return AADVariable(n_val,n_der,name=name)

def tan(obj: AADVariable) -> AADVariable:
    """TAN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.tan(val)
    n_der = val * 1/(np.cos(val)**2)
    return AADVariable(n_val,n_der,name=name)

def arcsin(obj: AADVariable) -> AADVariable:
    """ARCSIN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arcsin(val)
    n_der = val * 1/(sqrt(1-(val**2)))
    return AADVariable(n_val,n_der,name=name)

def arccos(obj: AADVariable) -> AADVariable:
    """ARCCOS OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arccos(val)
    n_der = val * -1/(sqrt(1-(val**2)))
    return AADVariable(n_val,n_der,name=name)

def arctan(obj: AADVariable) -> AADVariable:
    """ARCTAN OPERATOR: RETURNS AAD-VARIABLE TYPE"""
    name = obj.name
    val = obj.val
    der = obj.der
    n_val = np.arccos(val)
    n_der = val * -1/(sqrt(1-(val**2)))
    return AADVariable(n_val,n_der,name=name)


x = AADVariable(3.14159265358/2)
print(sin(x))
print(3*x + 5)

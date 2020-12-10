import numpy as np
from AADFunction import AADFunction
from AAD import AADVariable

"""
The AAD_Newton method solver.
Provides a static solve function.
"""
class AAD_Newton:
    @staticmethod
    def solve(lambda_function, x0, converge_delta = 1e-5, max_iter = 100):
        """
        Returns a solution for a given lambda vector-valued function (if scalar, wrap it in array) using Newton's method with AAD core.

        Inputs
        -----------
        lamda_funciton      : function
                            list of function to be solved for. Each function may contain more than one AADVariable
        x0                  : list
                            list of initial contidition values
        convergence_delta   : float 
                            convergence minimum error parameter. This dictates what an acceptable change in the iteration is. Default value 1e-5
        max_iter            : float
                            maximimum number of iterations before stopping the algorith. Default value 100.

        Outputs
        -----------
        out                 : list
                            list of values for the converged result. This is the solution output by the newton solver.


        Examples
        -------------
        >>> AAD_Newton.solve(lambda x, y, z, a: [x+4*y-z+a, a-2, y*5+z*0.1, x+2*a], [1, 0, 1, 1])
        [-4.0, 0.03703703703703704, -1.851851851851852, 2.0]

        >>> AAD_Newton.solve(lambda x, y: [x*y+1, 3*x+5*y-1], [1, 1])
        [-1.1350416126511096, 0.8810249675906657]

        >>> AAD_Newton.solve(lambda x: [x**2-3], [1])
        [1.7320508075688772]
        """

        nxs = len(x0)
        # the initial guess x0 must not be 0, 0 or the solution will diverge. preprocess this
        x0 = [x + 0.1 if x == 0 else x for x in x0]
        xs = [AADVariable(x0[i], [1 if j == i else 0 for j in range(nxs)]) for i in range(nxs)]
        
        f = AADFunction(lambda_function(*xs))
        for i in range(max_iter):
            Jk = f.der()
            nfk = -np.array(f.val())

            # solve linear equation system for higher numerical stability
            if nxs > 1:
                sv = np.linalg.solve(Jk, nfk)
            else:
                sv = nfk/Jk
            # this is dxk
            
            xs = [xs[i] + sv[i] for i in range(nxs)] 

            f = AADFunction(lambda_function(*xs))
            # print(xs, sv, f)

            if max([s if s > 0 else -s for s in sv]) <= converge_delta:
                break
        return [x.val for x in xs]


import numpy as np
from scipy.sparse.linalg import gmres, LinearOperator
from AADFunction import AADFunction
from AAD import AADVariable


class AAD_GMRES:
    @staticmethod
    def solve(lambda_function, x0, converge_delta = 1e-5, max_iter = 100):
        """
        Returns a solution for a given lambda vector-valued function (if scalar, wrap it in array) using GMRES with AAD core.
        
        Input
        ------------
        lambda_function     : function
                            list of functions to be solved. Each function can be single variable or multivariate
        x0                  : list
                            list containing the initial value for each variable
        convergence_delta   : float 
                            convergence minimum error parameter. This dictates what an acceptable change in the iteration is. Default value 1e-5
        max_iter            : float
                            maximimum number of iterations before stopping the algorith. Default value 100.

        Outputs
        -----------
        out                 : list
                            list of values for the converged result. This is the solution output by the newton solver.

                            
        Example
        ------------
        >>> AAD_GMRES.solve(lambda x, y: [x+y+5, 3*x-y+1], [0.5, 1.5])
        [-1.5000000000000004, -3.500000000000001]
        >>> AAD_GMRES.solve(lambda x: [x-2], [300])
        [2.0]
        >>> AAD_GMRES.solve(lambda x, y, z, a: [x+4*y-z+a, a-2, y*5+z*0.1, x+2*a], [1, 0, 1, 1])
        [-4.000000000000002, 0.03703703703703712, -1.8518518518518494, 2.0000000000000013]
        """

        nxs = len(x0)
        # the initial guess x0 must not be 0, 0 or the solution will diverge. preprocess this
        x0 = [x + 0.1 if x == 0 else x for x in x0]
        xs = [AADVariable(x0[i], [1 if j == i else 0 for j in range(nxs)]) for i in range(nxs)]
        
        f = AADFunction(lambda_function(*xs))
        for i in range(max_iter):
            negfk = -np.array(f.val())
            Jk = f.der()
            j_act = LinearOperator((nxs, nxs), matvec=lambda v: np.dot(Jk, v))
            dxk = gmres(j_act, negfk)[0]

            # update values
            for i in range(nxs):
                xs[i].val = xs[i].val + dxk[i]

            f = AADFunction(lambda_function(*xs))

            if max(dxk) <= converge_delta:
                break

        return [x.val for x in xs]

import numpy as np
from scipy.sparse.linalg import gmres, LinearOperator

class AAD_GMRES:
    @staticmethod
    def solve(lambda_function, x0, converge_delta = 1e-5, max_iter = 100):
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

# example usage:
# from AAD.solvers import AAD_GMRES
#
# so multivariates are handled correct please pass in a lambda function for faux symbolic math
#print(AAD_GMRES.solve(lambda x, y: [x+y+5, 3*x-y+1], [0.5, 1.5])) # [-1.5, -3.5]
#print(AAD_GMRES.solve(lambda x: [x-2], [300])) # [2.0]
#print(AAD_GMRES.solve(lambda x, y, z, a: [x+4*y-z+a, a-2, y*5+z*0.1, x+2*a], [1, 0, 1, 1]))

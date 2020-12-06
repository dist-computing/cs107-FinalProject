import numpy as np
from AADFunction import AADFunction
from AAD import AADVariable

class AAD_Newton:
    @staticmethod
    def solve(lambda_function, x0, converge_delta = 1e-5, max_iter = 100):
        nxs = len(x0)
        # the initial guess x0 must not be 0, 0 or the solution will diverge. preprocess this
        x0 = [x + 0.1 if x == 0 else x for x in x0]
        xs = [AADVariable(x0[i], [1 if j == i else 0 for j in range(nxs)]) for i in range(nxs)]
        
        f = AADFunction(lambda_function(*xs))
        for i in range(max_iter):
            Jk = f.der()
            negfk = -np.array(f.val())

            # solve linear equation system for higher numerical stability
            if nxs > 1:
                sv = np.linalg.solve(Jk, negfk)
            else:
                sv = negfk/Jk
            # this is dxk
            
            xs = [xs[i] + sv[i] for i in range(nxs)] 

            f = AADFunction(lambda_function(*xs))
            # print(xs, sv, f)

            if max([s if s > 0 else -s for s in sv]) <= converge_delta:
                break
        return [x.val for x in xs]

#print(AAD_Newton.solve(lambda x, y, z, a: [x+4*y-z+a, a-2, y*5+z*0.1, x+2*a], [1, 0, 1, 1])) # [-4.0, 0.03703703703703704, -1.851851851851852, 2.0]
#print(AAD_Newton.solve(lambda x, y: [x*y+1, 3*x+5*y-1], [1, 1])) # two sets of roots but [-1.1350416126511096, 0.8810249675906657]
#print(AAD_Newton.solve(lambda x: [x**2-3], [1])) # two sets of roots but [-1.1350416126511096, 0.8810249675906657]

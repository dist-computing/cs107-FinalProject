import copy
import numpy as np
from AAD import AADVariable
import AAD as AD

class AAD_grad:
    '''Peformes gradient descent on vector function with multiple variables.
    Only object is solve
    '''
    @staticmethod
    def solve(func, init, gamma, max_iter=10**5, convergence_delta = 10**-6, progress_step=None):
        '''Minimize functio using a gradient descent method
        
        Input
        -------------

        func         : function
                        vector function to be minimized. It is expected that this function
                        uses the AAD structure provided by the AAD package.
        init         : list 
                       initial values passed in as a list. Accepts only AADVariable objects as
                        initial values. If function only has one value, pass list of one value [x]
        gamma        : int or float
                        step-size hyper parameter for the nimerical model.
        max_iter     : float 
                        maximum number of iterations before quitting. Default value: 10**5
        convergence_delta    : float
                        minimum precision requested for convergence. Default value: 10**-6
        progress_step: int
                        prints out progres every number of steps. If none passed, nothing is printed.
                        Default value: None

        Output 
        -------------

        a            : list 
                        list of AADVariables with resultant minimum.


        Example
        -------------
        >>> x = AADVariable(3, [1 ,0])
        >>> y = AADVariable(2, [0, 1]) 

        >>> AAD_grad.solve(lambda X: AD.abs(2*X[0]-12+2*X[1]**2),[x,y],0.001,max_iter=10000)
        [AADVariable fun = 2.972000000000003, der = [1 0], AADVariable fun = 1.7456836263447164, der = [0 1]]
        >>> AAD_grad.solve(lambda X: AD.abs(2*X[0]-12),[x],0.001,max_iter=10000)
        [AADVariable fun = 5.99999999999967, der = [1 0]]
        >>> AAD_grad.solve(lambda X: AD.abs(AD.cos(X[0])*X[1]-12),[x,y],0.01,max_iter=10000)
        [AADVariable fun = 2.0851576460966394e-59, der = [1 0], AADVariable fun = 11.99691984276826, der = [0 1]]
        

        '''
        #create a copy of the initialized variables into the main a
        a=copy.deepcopy(init)
        #initialize the iteration counter
        i=0

        #run iterator until something triggers a return
        while True:
            # create a copy of the isntance 
            a_old=copy.deepcopy(a)

            #compute the gradient
            grad=func(a).der

            #initialize the difference vector
            diff=[]

            #iterate over all values of the vector
            for j in range(len(a)):
                # compute the new value for a for a particular vector entry. use gradient and gamma as step to updated value
                a[j] = a[j]-gamma*grad[j]
                #compute the difference value for convergence computation
                diff.append(a[j].val-a_old[j].val)
            
            #updated the number of iterations
            i+=1

            #obtain a convergence metric by getting the norm of the difference vector
            convergence=np.linalg.norm(diff)

            #printing the progress over the iterations for certain steps, not all steps
            if not progress_step == None and i%progress_step==0:
                print(f'Iteration: {i} | Convergence: {convergence}| Func Val:{func(a).val}')
            
            #if convergence is reached or if the number of iterations exceeds the maximum number of iteractions stop and retrun value
            if convergence<=convergence_delta or i>=max_iter:
                return a

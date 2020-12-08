import copy
import numpy as np

class AAD_grad:
    @staticmethod
    def solve(func, init, gamma, max_iter=10**5, precision = 10**-6, progress_step=None):
        
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
            if convergence<=precision or i>=max_iter:
                return a

# EXAMPLES

# x = AADVariable(3, [1 ,0])
# y = AADVariable(2, [0, 1]) 

# print(AAD_grad.solve(lambda X: abs(2*X[0]-12+2*X[1]**2),[x,y],0.001,progress_step=1000,max_iter=10000))
# print(AAD_grad.solve(lambda X: abs(2*X[0]-12),[x],0.001,progress_step=1000,max_iter=10000))
# print(AAD_grad.solve(lambda X: abs(cos(X[0])*X[1]-12),[x,y],0.01,progress_step=1000,max_iter=10000))

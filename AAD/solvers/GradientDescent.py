import copy
import numpy as np

def grad(func, init, gamma, max_iter=10000, precision = 10**-6, progress_step=None):
    a=copy.deepcopy(init)
    i=0
    while True:
        a_old=copy.deepcopy(a)
        grad=func(a).der
        # print(grad)

        diff=[]

        for j in range(len(a)):
            a[j] = a[j]-gamma*grad[j]
            diff.append(a[j].val-a_old[j].val)
        

        i+=1
        convergence=np.linalg.norm(diff)


        if not progress_step == None and i%progress_step==0:
            print(f'Iteration: {i} | Convergence: {convergence}| Func Val:{func(a).val}')
        
        if convergence<=precision or i>=max_iter:
            return a

# x = AADVariable(3, [1 ,0])
# y = AADVariable(2, [0, 1]) 

# print(grad(lambda X: abs(2*X[0]-12+2*X[1]**2),[x,y],0.001,progress_step=1000,max_iter=10000))
# print(grad(lambda X: abs(2*X[0]-12),[x],0.001,progress_step=1000,max_iter=10000))
# print(grad(lambda X: abs(cos(X[0])*X[1]-12),[x,y],0.01,progress_step=1000,max_iter=10000))

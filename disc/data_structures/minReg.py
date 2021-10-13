from gurobipy import *
import numpy as np
import copy

# Given a non-minimal region, computes a decomposition into minimal regions, returns them as list
def getMinRegions(x,y,A,Ap, log):
    print('teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest')
    R=[]
    x = [int(el) for el in x]
    y = [int(el) for el in y]

    print(x,y)
    while(True):
        xs,ys = solveMinRegILP(x,y,A,Ap,log)
        # if the region was already minimal
        if sum([x[i]-int(xs[i]) for i in range(len(x))]) == 0 and sum([y[i]-int(ys[i]) for i in range(len(y))]) == 0:
            break
        R.append((xs,ys))
        print('-----------FOUND SUBREGION:', xs, ys)
        x = [x[i]-int(xs[i]) for i in range(len(x))]
        y = [y[i]-int(ys[i]) for i in range(len(y))]

    R.append((x,y))
    return R

def solveMinRegILP(x,y,A,Ap, log):
    num_act = len(x)
    model2 = Model("minreg")
    x_s = model2.addMVar(num_act, vtype=GRB.BINARY)
    y_s = model2.addMVar(num_act, vtype=GRB.BINARY)
    model2.modelSense = GRB.MINIMIZE
    
    model2.update()

    model2.setObjective( sum(A[i,:]@x_s for i in range(num_act)) + sum(A[i,:]@y_s for i in range(num_act)))
    #model2.setObjective(np.ones(num_act) @ x_s)
    model2.update()

    model2.addConstr(Ap@x_s - A@y_s >= np.zeros(A.shape[0], dtype=int))
    model2.addConstr(x_s.sum()+y_s.sum() >= 1)
    for i in range(num_act):
        model2.addConstr(x_s[i] <= x[i])
        model2.addConstr(y_s[i] <= y[i])

    # Completion constraints
    for par in log:
        par_pref = copy.deepcopy(par)
        # Last activity of a terminal word is always the artificial end act
        par_pref[num_act-1] = 0
        model2.addConstr(par_pref @ x_s - par @ y_s == 0)

    model2.optimize()

    if model2.status != GRB.OPTIMAL:
        print(x,y)
        return x,y

    return x_s.X, y_s.X
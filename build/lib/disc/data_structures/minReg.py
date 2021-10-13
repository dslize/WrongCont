from gurobipy import *
import numpy as np

# Given a non-minimal region, computes a decomposition into minimal regions, returns them as list
def getMinRegions(x,y,A,Ap):
    print('teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest')
    R=[]
    x = [int(el) for el in x]
    y = [int(el) for el in y]
    while(True):
        xs,ys = x,y
        # if the region was already minimal
        if [x[i]-int(xs[i]) for i in range(len(x))].sum() == 0 and [y[i]-int(ys[i]) for i in range(len(y))].sum() == 0:
            break
        R.append((xs,ys))
        x = [x[i]-int(xs[i]) for i in range(len(x))]
        y = [y[i]-int(ys[i]) for i in range(len(y))]

    R.append((x,y))
    return R

def solveMinRegILP(x,y,A,Ap):
    num_act = len(x)
    model2 = Model("minreg")
    x_s = model2.addMVar(num_act, vtype=GRB.BINARY)
    y_s = model2.addMVar(num_act, vtype=GRB.BINARY)
    model2.modelSense = GRB.MINIMIZE
    
    model2.update()

    model2.setObjective( sum(A@(x_s-y_s)) )
    #model.setObjective(sum(A[i,:]@(x_s-y_s) for i in range()))
    model2.update()

    model2.addConstr(Ap@x_s - A@y_s >= np.zeros(A.shape[0], dtype=int))
    model2.addConstr(x_s.sum()+y_s.sum() >= 1)
    for i in range(num_act):
        model2.addConstr(x_s[i] <= x[i])
        model2.addConstr(y_s[i] <= y[i])
    #model.addConstr(x_s <= x)
    #model.addConstr(y_s <= y)

    model2.optimize()

    return x_s.X, y_s.X
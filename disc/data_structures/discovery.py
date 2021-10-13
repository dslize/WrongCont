from gurobipy import *
import numpy as np
import copy

def solveGreedyILP(num_act, A, Ap, WC, wired, log, useSelfloop=False):

    model = Model("greedy")
    x = model.addMVar(num_act, vtype=GRB.BINARY)
    y = model.addMVar(num_act, vtype=GRB.BINARY)

    #z={}
    #for i in range(len(WC)):
    #    z[i] = model.addVar(vtype=GRB.BINARY)

    z = model.addMVar(len(WC), vtype=GRB.BINARY)

    model.modelSense = GRB.MINIMIZE
    
    model.update()

    model.setObjective(3*num_act*z.sum() + x.sum() + y.sum())
    model.update()

    model.addConstr(Ap@x - A@y >= np.zeros(A.shape[0], dtype=int))

    for i,j in wired:
        model.addConstr(x[i] + y[j] <= 1)

    for i, (pwt, pw) in enumerate(WC):
        model.addConstr(pw @ x - pwt @ y <= z[i] * pwt.sum() - 1) # len of wt

    # forbid selfloops if specified
    if useSelfloop == False:
        for i in range(num_act):
            model.addConstr(x[i] + y[i] <= 1)

    # Completion constraints
    for par in log:
        par_pref = copy.deepcopy(par)
        # Last activity of a terminal word is always the artificial end act
        par_pref[num_act-1] = 0
        model.addConstr(par_pref @ x - par @ y == 0)

    # Limit number of edges for a place, unfort hard coded
    #model.addConstr(x.sum() + y.sum() <= 3)

    model.optimize()

    return x.X, y.X, z.X

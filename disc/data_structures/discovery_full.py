from gurobipy import *
import numpy as np
import copy

def solveFullILP(num_act, A, Ap, WC, log, useSelfLoop=False):
    model = Model("full")

    X = {}
    Y = {}
    for i in range(num_act ** 2):
        X[i] = model.addMVar(num_act, vtype=GRB.BINARY)
        Y[i] = model.addMVar(num_act, vtype=GRB.BINARY)

    z = model.addMVar(len(WC), vtype=GRB.BINARY)

    Z = {}
    for i in range(num_act ** 2):
        Z[i] = model.addMVar(len(WC), vtype=GRB.BINARY)

    model.modelSense = GRB.MINIMIZE
    model.update()

    model.setObjective(3*(num_act**3)*z.sum() + sum(X[i].sum() for i in range(num_act ** 2)) + sum(Y[i].sum() for i in range(num_act ** 2)))
    model.update()

    # Discover only feasible places
    for i in range(num_act**2):
        model.addConstr(Ap@X[i] - A@Y[i] >= np.zeros(A.shape[0], dtype=int))

    # Force optimal solution to be unique in order
    for i in range(num_act**2)-1:
        model.addConstr(X[i] >= X[i+1])
        model.addConstr(Y[i] >= Y[i+1])

    # Uniwiredness constraints
    # for i in range(num_act ** 2):
    #    for j in range(num_act ** 2):
    #        if i == j:
    #            continue
    #        else:
    #            xi = X[i]
    #            yi = Y[i]
    #            xj = X[j]
    #            yj = Y[j]
    #            for k in range(num_act):
    #                for l in range(num_act):
    #                    model.addConstr(xi[k] + yi[l] + xj[k] + yj[l] <= 3)

    # Completion constraints
    for par in log:
        par_pref = copy.deepcopy(par)
        # Last activity of a terminal word is always the artificial end act
        par_pref[num_act-1] = 0
        for i in range(num_act ** 2):
            model.addConstr(par_pref @ X[i] - par @ Y[i] == 0)

    # Store in variables if wrong continuations are separated, value 0 means sep.
    for i in range(num_act ** 2):
        zi = Z[i]
        for j, (pwt, pw) in enumerate(WC):
            model.addConstr(pw @ X[i] - pwt @ Y[i] <= zi[j] * pwt.sum() - 1) # len of wt

    # set z variable to store if any place separates a wrong continuation
    for j in range(len(WC)):
        model.addConstr(sum(Z[i][j] for i in range(num_act ** 2)) - (num_act ** 2) <= z[j] - 1)

    # forbid selfloops if specified
    if useSelfLoop == False:
        for i in range(num_act**2):
            xi = X[i]
            yi = Y[i]
            for j in range(num_act):
                model.addConstr(xi[j] + yi[j] <= 1)

    model.optimize()

    return [X[i].X for i in range(num_act**2)], [Y[i].X for i in range(num_act**2)], z.X
from disc.data_structures.trie import TrieNode, get_parikh, add_seq, get_prefix_lang
from disc.data_structures.discovery import solveGreedyILP
from disc.data_structures.minReg import getMinRegions, solveMinRegILP
from disc.data_structures.sequenceDB import *
import numpy as np
import copy
import gurobipy as grb

def update_wired(wired, x, y):
    genx = list(idx for idx, val in enumerate(x) if val==1)
    geny = list(idx for idx, val in enumerate(y) if val==1)
    for ti in genx:
        for tj in geny:
            wired.append((ti,tj))

#expects sdb as input
def computeRegions(sdb):
    root = TrieNode()
    par_log = []
    num_act = sdb.num_activities

    log = sdb.db
    for seq in log:
        par = add_seq(seq, num_act, root)
        par_log.append(par)

    A, Ap, WC = get_prefix_lang(root)
    A = np.array(A)
    Ap = np.array(Ap)

    wired= []
    X= []
    Y=[]
    count=0

    while(True):
        count = count+1
        print("--------------------------------------- Iteration " + str(count))
        x, y, z = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
        #print(x)
        #print(y)
        #print(z)

        # if trivial region
        if int(x.sum()+y.sum()) == 0:
            break
        # if no wrong continuations separated
        if z.sum() == len(z):
            break

        R = getMinRegions(x,y,A,Ap,par_log)
        #R=[(x,y)]
        
        for (xs,ys) in R:
            X.append(xs)
            Y.append(ys)
            update_wired(wired,xs,ys)

        tmp = [wc for idx,wc in enumerate(WC) if z[idx]==1]
        WC = tmp

    print('number of remaining wrong cont: ', len(WC))
    
    return X,Y

# input is EventLog, output is regions
def computeRegions_log(eventlog):
    sdb=log_to_sdb(eventlog)
    X,Y = computeRegions(sdb)

    return X,Y

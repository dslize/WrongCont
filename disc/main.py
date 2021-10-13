from disc.data_structures.trie import TrieNode, get_parikh, add_seq, get_prefix_lang
from disc.data_structures.discovery import solveGreedyILP
from disc.data_structures.minReg import getMinRegions, solveMinRegILP
from disc.algo import *
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from disc.build_petri import *
import numpy as np
import copy
import gurobipy as grb

def build_petri():
    return

# def update_wired(wired, x, y):
#     genx = list(idx for idx, val in enumerate(x) if val==1)
#     geny = list(idx for idx, val in enumerate(y) if val==1)
#     for ti in genx:
#         for tj in geny:
#             wired.append((ti,tj))

# root = TrieNode()
# par_log = []
# num_act = 5

# log = [[0,2,3],[1,2,4]]
# for seq in log:
#     par = add_seq(seq, num_act, root)
#     par_log.append(par)

# A, Ap, WC = get_prefix_lang(root)
# A = np.array(A)
# Ap = np.array(Ap)

# wired= []
# X= []
# Y=[]

# while(True):
#     #print("------ Iteration " + str(6-count))
#     x, y, z = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#     #print(x)
#     #print(y)
#     #print(z)

#     # if trivial region
#     if int(x.sum()+y.sum()) == 0:
#         break
#     # if no wrong continuations separated
#     if z.sum() == len(z):
#         break

#     R = getMinRegions(x,y,A,Ap,par_log)
    
#     for (xs,ys) in R:
#         X.append(xs)
#         Y.append(ys)
#         update_wired(wired,xs,ys)

#     tmp = [wc for idx,wc in enumerate(WC) if z[idx]==1]
#     WC = tmp

# for i in range(len(X)):
#     print(X[i], Y[i])

from pm4py.objects.log.importer.xes import importer as xes_importer

########################################################################  CHANGE FILE HERE
log = xes_importer.apply('repairExample.xes')
########################################################################

#X,Y = computeRegions_log(log)
sdb=log_to_sdb(log)
sdb.idx_to_activity[sdb.num_activities] = "artificial_start"
sdb.idx_to_activity[sdb.num_activities+1] = "artificial_end"
X,Y = computeRegions(sdb)

sdb.num_activities = sdb.num_activities+2

for i in range(len(X)):
    print(X[i], Y[i])

# #for i in range(sdb.num_activities):
print("----- PLACES ------")
for i in range(len(X)):
    x=X[i]
    y=Y[i]

    print('--ingoing activities:')
    for i in range(sdb.num_activities):
        if x[i] == 1:
            print(sdb.idx_to_activity[i])
    print('--outgoing activities')
    for i in range(sdb.num_activities):
        if y[i] == 1:
            print(sdb.idx_to_activity[i])
    print('---- next place')

net, init, final = build_petrinet(sdb,X,Y)

gviz = pn_visualizer.apply(net, init, final)
pn_visualizer.view(gviz)

#from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
#fitness = replay_fitness_evaluator.apply(log, net, init, final, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)

#print(fitness)
from disc.data_structures.trie import TrieNode, get_parikh, add_seq, get_prefix_lang
from disc.data_structures.discovery_full import solveFullILP
import numpy as np
import copy
import gurobipy as grb

def pretty_print(WC, mask=[]):
    if len(mask) == 0:
        mask = [0] * len(WC)
    for idx, (wt,w) in enumerate(WC):
        #skip printing wrong con if mask the mask has value 1
        if mask[idx] == 1: continue 
        wroncon = []
        for i in range(len(wt)):
            if wt[i]>0:
                for _ in range(wt[i]):
                    wroncon.append(i)
        print(wroncon)

root = TrieNode()
par_log = []
seq = [0,2,3]
num_act = 5

def update_wired(wired, x, y):
    genx = list(idx for idx, val in enumerate(x) if val==1)
    geny = list(idx for idx, val in enumerate(y) if val==1)
    for ti in genx:
        for tj in geny:
            wired.append((ti,tj))

par1 = add_seq(seq, num_act, root)
par_log.append(par1)

#seq2 = [1,3,5,5]
#add_seq(seq2, num_act, root)

#seq3 = [0,1]
seq3 = [1,2,4]
par2 = add_seq(seq3, num_act, root)
par_log.append(par2)

A, Ap, WC = get_prefix_lang(root)
A = np.array(A)
Ap = np.array(Ap)

x, y, z = solveFullILP(num_act+2, A, Ap, WC, par_log, True)
for i in range(len(x)):
    print(x[i], y[i])

print(z)
pretty_print(WC,z)
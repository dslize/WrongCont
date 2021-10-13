from disc.data_structures.trie import TrieNode, get_parikh, add_seq, get_prefix_lang
from disc.data_structures.discovery import solveGreedyILP
import numpy as np
import copy
import gurobipy as grb

print('test')

def pretty_print(WC, mask=[]):
    if len(mask) == 0:
        mask = [0] * len(WC)
    for idx, (wt,w) in enumerate(WC):
        #skip prointing wrong con if mask the mask has value 1
        if mask[idx] == 1: continue 
        wroncon = []
        for i in range(len(wt)):
            if wt[i]>0:
                for _ in range(wt[i]):
                    wroncon.append(i)
        print(wroncon)

root = TrieNode()
par_log = []
#seq = [0,2,3]
seq = [0,2,3]
#num_act = 4
num_act = 5

def update_wired(wired, x, y):
    genx = list(idx for idx, val in enumerate(x) if val==1)
    geny = list(idx for idx, val in enumerate(y) if val==1)
    for ti in genx:
        for tj in geny:
            wired.append((ti,tj))

par1 = add_seq(seq, num_act, root)
par_log.append(par1)

#seq3 = [0,1]
seq3 = [1,2,4]
par2 = add_seq(seq3, num_act, root)
par_log.append(par2)

s = copy.deepcopy(seq3)
add_seq(s, num_act, root)

# NOTE: WC LIST TOO LONG WHEN MULTIPLE EQUAL TRACES, TRC VARIANTS??

print(root.act)
#for child in root.children[2].children:
for child in root.children:
    if child != 0:
        print(child.act)

#print(root.children[2].children[3].children[5].children[7].children)

print("-------\n", par_log, "\n -----------")

A, Ap, WC = get_prefix_lang(root)
A = np.array(A)
Ap = np.array(Ap)

#print(np.array(A))
#print(np.array(Ap))
#pretty_print(WC)
# print(A)

wired= []
#print(grb.gurobi.version())
# dont forget artificial activities now
x, y, z = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#print(x)
#print(y)
print(z)
print("--------\n Sep wc:")
pretty_print(WC, z)
print("--------\n All wc:")
pretty_print(WC)
print("--------\n Iteration 2")
#filter WC list with those ethat were separated
tmp = [wc for idx,wc in enumerate(WC) if z[idx]==1]
WC = tmp
update_wired(wired,x,y)
#print(wired)

x_2, y_2, z_2 = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#print(x_2)
#print(y_2)
print(z_2)
print("--------\n Sep wc:")
pretty_print(WC, z_2)
print("--------\n All wc:")
pretty_print(WC)

print("--------\n Iteration 3")
tmp = [wc for idx,wc in enumerate(WC) if z_2[idx]==1]
WC = tmp
update_wired(wired,x_2,y_2)
#print(wired)

x_3, y_3, z_3 = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#print(x_3)
#print(y_3)
print(z_3)
print("--------\n Sep wc:")
pretty_print(WC, z_3)
print("--------\n All wc:")
pretty_print(WC)

print("--------\n Iteration 4")
tmp = [wc for idx,wc in enumerate(WC) if z_3[idx]==1]
WC = tmp
update_wired(wired,x_3,y_3)
#print(wired)

x_4, y_4, z_4 = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#print(x_4)
#print(y_4)
print(z_4)
print("--------\n Sep wc:")
pretty_print(WC, z_4)
print("--------\n All wc:")
pretty_print(WC)

print("--------\n Iteration 5")
tmp = [wc for idx,wc in enumerate(WC) if z_4[idx]==1]
WC = tmp
update_wired(wired,x_4,y_4)
#print(wired)

x_5, y_5, z_5 = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#print(x_4)
#print(y_4)
print(z_5)
print("--------\n Sep wc:")
pretty_print(WC, z_5)
print("--------\n All wc:")
pretty_print(WC)
print("-----------------\n Places:")
print(x,y)
print(x_2,y_2)
print(x_3,y_3)
print(x_4,y_4)
print(x_5,y_5)
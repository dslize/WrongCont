from disc.data_structures.trie import TrieNode, get_parikh, add_seq, get_prefix_lang
from disc.data_structures.discovery import solveGreedyILP
from disc.data_structures.minReg import getMinRegions, solveMinRegILP
import numpy as np
import copy
import gurobipy as grb

def getMinRegionss(x,y,A,Ap):
    # print('teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest')
    R=[]
    x = [int(el) for el in x]
    y = [int(el) for el in y]
    print(type(x), type(A))
    while(True):
        xs,ys = x,y
        # if the region was already minimal
        if sum([x[i]-int(xs[i]) for i in range(len(x))]) == 0 and sum([y[i]-int(ys[i]) for i in range(len(y))]) == 0:
            break
        R.append((xs,ys))
        x = [x[i]-int(xs[i]) for i in range(len(x))]
        y = [y[i]-int(ys[i]) for i in range(len(y))]

    R.append((x,y))
    return R
    # print('teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest')
    # return [(x,y)]

print('test')

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

par = add_seq(seq, num_act, root)
par_log.append(par)

#seq2 = [1,3,5,5]
#add_seq(seq2, num_act, root)

#seq3 = [0,1]
seq3 = [1,2,4]
par1 = add_seq(seq3, num_act, root)
par_log.append(par1)

#s = copy.deepcopy(seq3)
#add_seq(s, num_act, root)

# NOTE: WC LIST TOO LONG WHEN MULTIPLE EQUAL TRACES, TRC VARIANTS??

print(root.act)
#for child in root.children[2].children:
for child in root.children:
    if child != 0:
        print(child.act)

#print(root.children[2].children[3].children[5].children[7].children)

A, Ap, WC = get_prefix_lang(root)
A = np.array(A)
Ap = np.array(Ap)

#print(np.array(A))
#print(np.array(Ap))
#pretty_print(WC)
# print(A)

wired= []
count = 5
X= []
Y=[]
# while(count>0):
#     print("------ Iteration " + str(6-count))
#     x, y, z = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
#     print(x)
#     print(y)
#     print(z)
#     X.append(x)
#     Y.append(y)
#     print("--------\n Sep wc:")
#     pretty_print(WC, z)
#     print("--------\n All wc:")
#     pretty_print(WC)
#     tmp = [wc for idx,wc in enumerate(WC) if z[idx]==1]
#     WC = tmp
#     update_wired(wired,x,y)
#     count -= 1

while(True):
    print("------ Iteration " + str(6-count))
    x, y, z = solveGreedyILP(num_act+2, A, Ap, WC, wired, par_log, False)
    print(x)
    print(y)
    print(z)
    # if trivial region
    if int(x.sum()+y.sum()) == 0:
        break
    # if no wrong continuations separated
    if z.sum() == len(z):
        break

    xc=copy.deepcopy(x)
    yc=copy.deepcopy(y)

    R = getMinRegions(x,y,A,Ap)
    #R = [(xc,yc)]
    print('wtfffffffffffffffffff22222')
    for (xs,ys) in R:
        X.append(xs)
        Y.append(ys)
        update_wired(wired,xs,ys)
    print("--------\n Sep wc:")
    pretty_print(WC, z)
    print("--------\n All wc:")
    pretty_print(WC)
    tmp = [wc for idx,wc in enumerate(WC) if z[idx]==1]
    WC = tmp
    count -= 1



print("---------- Final set of regions")
for i in range(len(X)):
    print(X[i], Y[i])

print(wired)
print(int(x.sum()+y.sum()) == 0)
import numpy as np
import copy

def get_parikh(seq, num_act):
    # Assumes the elements of seq range from 0 to num_act-1
    res = np.zeros(num_act, dtype=int)
    for i in range(len(seq)):
        res[seq[i]] += 1
    return res

class TrieNode:
    # children if non existent 0, otherwise a TrieNode object
    def __init__(self):
        self.act = -1
        self.parikh = np.array([])
        self.children = []

# Adds sequence to the given tree, returns parikh vector of word to be added
def add_seq(seq, num_act, root):
    #debug: copy not needed?? only for debugging trying to insert same seq twice
    seqc = copy.deepcopy(seq)
    #add artificial start/end activity
    seqc.insert(0,num_act)
    seqc.append(num_act+1)

    #If first word
    if root.act == -1:
        root.act = num_act
        par = np.zeros(num_act+2, dtype=int)
        par[num_act]=1
        root.parikh = par
        root.children = [0] * (num_act+2)
    
    add_suffix(seqc[1:], num_act+2, root)
    return get_parikh(seqc, num_act+2)

def add_suffix(seq, num_act, node):
    if len(seq) == 0:
        return
    else:
        #If child does not yet exist
        if node.children[seq[0]] == 0:
            child = TrieNode()
            child.act = seq[0]
            par = np.copy(node.parikh)
            par[seq[0]] += 1
            child.parikh = par
            child.children = [0] * num_act
            node.children[seq[0]] = child
        
        add_suffix(seq[1:], num_act, node.children[seq[0]])

#Returns two lists of parikh vectors, A and A', and also the list of tuples of parikh vectors of wrong conts and minus last activity
def get_prefix_lang(root):
    A = []
    Ap = []
    WC = []

    #Initialise wrong conts with all traces not starting with artificial start activity
    num_act = len(root.children)
    for i in range(num_act):
        w = np.zeros(num_act, dtype=int)
        wt = np.zeros(num_act, dtype=int)

        wt[i] = 1
        WC.append((wt,w))
    # Remove the parikh vector containing just the start activity, always not a wrong cont in non empty log
    del WC[-2]

    traverse_append_trie(A, Ap, WC, root)
    return A, Ap, WC

# Adds parikh vectors of nodes and their prefix to matrices A, Ap; computes wrong continuations
def traverse_append_trie(A, Ap, WC, node):
    A.append(np.copy(node.parikh))
    pre = np.copy(node.parikh)
    pre[node.act] -= 1
    Ap.append(pre)

    for i in range(len(node.children)):
        if node.children[i] != 0:
            traverse_append_trie(A, Ap, WC, node.children[i])
        #otherwise add wrong cont
        else:
            w = np.copy(node.parikh)
            wt = np.copy(node.parikh)
            wt[i] += 1
            WC.append((wt,w))
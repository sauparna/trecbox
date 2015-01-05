import sys
import math
import numpy as np
import scipy.stats as stats
import fileinput as fin
from collections import OrderedDict as od 
import simplejson as json
import os

def print_summary(s, f=None):
    # s = [M, V, E, Z, L, U]
    fp = None
    if f:
        fp = open(f, "w")
    fmt = "{:>7} {:>7} {:>7} {:>7} {:>7} {:>7}"
    print(fmt.format("M", "V", "E", "Z", "L", "U"), file=fp)
    fmt = "{:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f}"
    print(fmt.format(*s), file=fp)
    if fp:
        fp.close()
    
def print_datatab(tab, f=None):
    fp = None
    if f:
        fp = open(f, "w")
    fmt = "{:>10} {:>5} {:>7}"
    print(fmt.format("testcol", "topic", "score"), file=fp)
    fmt = "{:>10} {:>5} {:>7.4f}"
    for i in range(len(tab)):
        print(fmt.format(tab[i][0], tab[i][1], tab[i][2]), file=fp)
    if fp:
        fp.close()

def print_metatab(tab, f=None):
    fp = None
    if f:
        fp = open(f, "w")

    fmt = "{:>10} {:>7}{:>7}{:>7} {:>7}{:>7}{:>7} {:>7}{:>7}{:>8}{:>8} {:>8}{:>8}"
    print(fmt.format("testcol", "m1","s1","n1",  "m2","s2","n2",
                     "y","v","l","u", "w","W"),
          file=fp)

    for i in range(len(tab)):
        fmt = "{:>10} {:>7.4f}{:>7.4f}{:>7d} {:>7.4f}{:>7.4f}{:>7d} {:>7.4f}{:>7.4f}{:>8.4f}{:>8.4f} {:>8.4f}{:>8.4f}"
        print(fmt.format(tab[i][0], 
                         tab[i][1],tab[i][2],int(tab[i][3]), 
                         tab[i][4],tab[i][5],int(tab[i][6]), 
                         tab[i][7],tab[i][8],tab[i][9],tab[i][10],
                         tab[i][11],tab[i][12]), 
              file=fp)

    if fp:
        fp.close()

def sd_pooled(s1, s2, n1, n2):
    return (((n1 - 1) * s1**2 + (n2 - 1) * s2**2)/(n1 - 1 + n2 - 1)) ** 0.5

def tau2(_y, _w, k):
    _wy2 = []
    _wy  = []
    _w2  = []
    for i in range(len(_w)):
        w = _w[i]
        y = _y[i]
        _wy2.append(w * y**2)
        _wy.append(w * y)
        _w2.append(w**2)
    Q  = sum(_wy2) - (sum(_wy)**2) / sum(_w)
    df = k - 1
    if Q < df:
        return 0.0
    C  = sum(_w) - sum(_w2) / sum(_w)
    T2 = (Q - df) / C
    return T2

def gobble(files):
    # evals[f.m.t] = s
    evals = od()
    for l in fin.input(files):
        f = os.path.basename(fin.filename())
        m,t,s = l.split()
        if t == "all":
            continue
        k = ".".join([f,m,t])
        evals[k] = float(s)
        # if f not in evals:
        #     evals[f] = od()
        # if m not in evals[f]:
        #     evals[f][m] = od()
        # evals[f][m][t] = s
    return evals

# # BITMAP
# doc stem algorithm measure score
# d s a m t
# 0 0 1 1 0

# # BIGMAP
# doc       = []
# stemming  = [1 "n",     2 "p"]
# algorithm = [1 "bm25",  2 "sersimple", 3 "dhgb3",
#              4 "tfidf", 5 "tfidf2",    6 "tfidf8", 7 "tfidf9"],
# measure   = [1 "map",   2 "bpref"]
# topic     = []

bigmap = [[],
          ["n", "p"],
          ["bm25", "sersimple", "dhgb3",
           "tfidf", "tfidf2", "tfidf8", "tfidf9"],
          ["map"],
          []
         ]

def table(evals, bmp="01110"):
    # tab = [testcol, topic, score]
    bitmap = [int(x) for x in list(bmp)]

    pos = []
    var = []
    for i in range(len(bitmap)):
        if bitmap[i] != 0:
            pos.append(i)
        else:
            var.append(i)

    tab = []
    for k in evals:
        row = []
        match = 0
        part = k.split(".")
        for i in range(len(pos)):
            if part[pos[i]] == bigmap[pos[i]][bitmap[pos[i]]-1]:
                match += 1
        if match == len(pos):
            for j in range(len(var)):
                row.append(part[var[j]])
            row.append(evals[k])
            tab.append(row)
    return tab

# an annotated vector
def avector(tab):
    # From [t, q, s] to {t: {q: s}}
    d = {}
    for i in range(len(tab)):
        t = tab[i][0]; q = tab[i][1]; s = tab[i][2]
        if t not in d:
            d[t] = {}
        d[t][q] = s
    return d

def compute(d1, d2, es="RR", model="RE"):
    # d = {t: {q: s}}

    tab = []
    sum_wy = 0.0
    sum_w  = 0.0

    for t in d1:
        v1  = np.fromiter(d1[t].values(), np.float)
        n1  = len(v1)
        s1  = v1.std(ddof=1)
        m1  = v1.mean()

        v2  = np.fromiter(d2[t].values(), np.float)
        n2  = len(v2)
        s2  = v2.std(ddof=1)
        m2  = v2.mean()

        s = ((n1 - 1) * s1 * s1 + (n2 - 1) * s2 * s2)/(n1 - 1 + n2 - 1)
        y = math.log(m2) - math.log(m1)
        v = s * (1 / (n1 * m1 * m1) + 1 / (n2 * m2 * m2))
        l = y - 1.96 * v**0.5
        u = y + 1.96 * v**0.5
        w = 1 / v
        
        #          [0  1   2   3   4   5   6   7  8  9  10 11]
        tab.append([t, m1, s1, n1, m2, s2, n2, y, v, l, u, w ])

    # # DEBUG
    # tab = [["Carroll", 94,22,60,  92,20,60,  0.095, 0.033, 30.352],
    #        ["Grant",   98,21,65,  92,22,65,  0.277, 0.031, 32.568],
    #        ["Peck",    98,28,40,  88,26,40,  0.367, 0.050, 20.048],
    #        ["Donat",   94,19,200, 82,17,200, 0.664, 0.011, 95.111],
    #        ["Stewart", 98,21,50,  88,22,45,  0.462, 0.043, 23.439],
    #        ["Young",   96,21,85,  92,22,85,  0.185, 0.023, 42.698]]

    k = len(tab)

    _y = []
    _w = []
    for i in range(len(tab)):
        y = 7
        w = 11
        _y.append(tab[i][y])
        _w.append(tab[i][w])

    T2 = tau2(_y, _w, k)

    for i in range(len(tab)):
        y = 7
        v = 8
        w = 1 / (tab[i][v] + T2)
        tab[i].append(w)

    ov = summary(tab)

    return tab, ov

def summary(tab, model="RE"):
    y = 7
    w = 12
    if model == "FE":
        w = 11
    _wy = []
    _w  = []
    for i in range(len(tab)):
       _wy.append(tab[i][w] * tab[i][y])
       _w.append(tab[i][w])
    M = sum(_wy) / sum(_w)
    V = 1 / sum(_w)
    E = V**0.5
    Z = M / E
    L = M - 1.96 * E
    U = M + 1.96 * E
    return [M, V, E, Z, L, U]

def main(argv):

    # Usage: meta.py path/to/evals/*

    evals = gobble(argv[1:])
    #print(json.dumps(evals, indent=2))
    # print(len(evals))

    # # DEBUG
    # tag  = ["n.p.bm25"]
    # code = [["01110", "02110"]]

    plan = [["NBM25.PBM25",     "nbm25.pbm25",      "01110", "02110"], 
            ["SERSIMPLE.TFIDF", "sersimple.tfidf8", "02210", "02610"], 
            ["TFIDF.TFIDF1",    "tfidf8.tfidf9",    "02610", "02710"],
            ["TFIDF.TFIDF2",    "tfidf8.tfidf2",    "02610", "02510"],
            ["TFIDF.TFIDF3",    "tfidf8.dhgb3",     "02610", "02310"]]

    for i in range(len(plan)):

        pre = plan[i][0]
        tag = plan[i][1]
        
        p1,p2 = tag.split(".")

        t1_ = pre + "." + p1 + "." + "v1"
        t2_ = pre + "." + p2 + "." + "v2"
        t_  = pre + "." + "meta"
        s_  = pre + "." + "summary"

        t1 = table(evals, plan[i][2])
        t2 = table(evals, plan[i][3])

        print_datatab(t1, t1_)
        print_datatab(t2, t2_)

        t,s = compute(avector(t1), avector(t2))

        print_metatab(t, t_)
        print_summary(s, s_)

if __name__ == "__main__":
    main(sys.argv)

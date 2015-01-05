import sys
import os
import math
import numpy as NP
from collections import OrderedDict as OD

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

def compute(mat):
    # mat = [testcol, topic, MAP1, MAP2]

    tab  = []
    prev = mat[0][0]

    v1 = []
    v2 = []

    for i in range(len(mat)):
        if mat[i][0] == prev and i < len(mat)-1:
            v1.append(mat[i][2])
            v2.append(mat[i][3])
            continue
        if i == len(mat)-1:
            v1.append(mat[i][2])
            v2.append(mat[i][3])
        n1 = len(v1)
        n2 = len(v2)
        m1 = NP.mean(v1)
        m2 = NP.mean(v2)
        s1 = NP.std(v1, ddof=1) # n-1 in denominator
        s2 = NP.std(v2, ddof=1)
        s  = ((n1 - 1) * s1 * s1 + (n2 - 1) * s2 * s2) / (n1 - 1 + n2 - 1)
        y  = math.log(m2 / m1)
        v  = s * (1 / (n1 * m1 * m1) + 1 / (n2 * m2 * m2))
        l  = y - 1.96 * v * v
        u  = y + 1.96 * v * v
        w  = 1 / v
        #          [0      1   2   3   4   5   6  7  8  9  10 11]
        tab.append([prev, m1, s1, n1, m2, s2, n2, y, v, l, u, w ])
        prev = mat[i][0]
        v1 = [mat[i][2]]
        v2 = [mat[i][3]]

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

    return tab

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
    m = math.exp(M)
    l = math.exp(L)
    u = math.exp(U)

    return [M, V, E, Z, L, U, m, l, u]

def print_summary(s, f=None):
    # s = [M, V, E, Z, L, U]                                                    
    fp = None
    if f:
        fp = open(f, "w")
    fmt = "{:>7} {:>7} {:>7} {:>7} {:>7} {:>7}  {:>7} {:>7} {:>7}"
    print(fmt.format("M", "V", "E", "Z", "L", "U", "m", "l", "u"), file=fp)
    fmt = "{:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f} {:>7.4f}  {:>7.4f} {:>7.4f} {:>7.4f}"
    print(fmt.format(*s), file=fp)
    if fp:
        fp.close()

def print_meta(tab, f=None):
    fp = None
    if f:
        fp = open(f, "w")
    fmt = "{:>10} {:>7}{:>7}{:>7} {:>7}{:>7}{:>7} {:>7}{:>7}{:>8}{:>8} {:>8}{:>\
8}"
    print(fmt.format("testcol", "m1","s1","n1",  "m2","s2","n2",
                     "y","v","l","u", "w","W"),
          file=fp)
    for i in range(len(tab)):
        fmt = "{:>10} {:>7.4f}{:>7.4f}{:>7d} {:>7.4f}{:>7.4f}{:>7d} {:>7.4f}{:>\
7.4f}{:>8.4f}{:>8.4f} {:>8.4f}{:>8.4f}"
        print(fmt.format(tab[i][0],
                         tab[i][1],tab[i][2],int(tab[i][3]),
                         tab[i][4],tab[i][5],int(tab[i][6]),
                         tab[i][7],tab[i][8],tab[i][9],tab[i][10],
                                          tab[i][11],tab[i][12]),
              file=fp)
    if fp:
        fp.close()

def print_matrix(mat, f=None):
    fp = None
    if f:
        fp = open(f, "w")
    fmt="{:<10} {:<10} {:<10} {:<10}"
    print(fmt.format("testcol", "topic", "MAP1", "MAP2"), file=fp)
    for i in range(len(mat)):
        fmt="{:<10} {:<10} {:<10.4f} {:<10.4f}"
        print(fmt.format(mat[i][0], mat[i][1], mat[i][2], mat[i][3]), file=fp)
    if fp:
        fp.close()

def matrix(f):
    # returns mat = [testcol, topic, MAP1, MAP2]
    mat = []
    with open(f, "r") as fp:
        next(fp)
        for l in fp:
            t,top,m1,m2 = [x.strip() for x in l.split()]
            mat.append([t, int(top), float(m1), float(m2)])
    return mat
        
def main(argv):
    # USAGE: meta.py <pairs dir> <meta dir>
    ind     = argv[1]
    outd    = argv[2]

    # # DEBUG
    # pairs = ["logtfnondl"]

    pairs    = ["stemtfidf", "tfidf", "noidf", "nondl", "logtfnondl", "logtf"]

    # mat  = [[testcol, topic, m1, m2], ...]
    # meta = [[testcol, m1, s1, n1, m2, s2, n2, y, v, l, u, w], ...]
    # ov   = [M, V, E, Z, L, U, m, l, u]

    for p in pairs:
        inf  = os.path.join(ind, p, p)
        outf = os.path.join(outd, p)
        mat  = matrix(inf)
        meta = compute(mat)
        ov   = summary(meta)
        print_matrix(mat, outf+".v") 
        print_meta(meta, outf+".m")
        print_summary(ov, outf+".s")
 
if __name__ == "__main__":
    main(sys.argv)

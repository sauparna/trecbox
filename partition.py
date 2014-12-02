#!/usr/bin/env python3

# Given a list of qids, the number of splits, the size of splits, it
# outputs a file for each list of qids in each split. The output is
# written to the directory passed as the last argument.

import sys
import os
from random import *
import simplejson as json

def knuth_shuffle(a):
    n = len(a)
    i = n - 1
    while (i >= 1):
        j = randint(0, i)
        t = a[j]
        a[j] = a[i]
        a[i] = t
        i -= 1
    return a

def read_list(f):
    l = open(f, "r").read().splitlines()
    l_ = []
    for i in range(len(l)):
        l_.append(int(l[i].split()[0]))
    return l_


def partition(qid, n, n_):
    # n = number of partitions
    # n_ = size of each partitions
    m = len(qid)
    if (n * n_) > m:
        print("unmanagable splits")
        return
    a = [None] * n
    q = set(qid)
    for i in range(n):
        a[i] = knuth_shuffle(list(q))[:n_]
        q = q - set(a[i])
    return a

def write_list(out_d, p):
    for i in range(len(p)):
        out_f = os.path.join(out_d, "p"+str(i+1))
        with open(out_f, "w") as fp:
            for j in range(len(p[i])):
                fp.write(str(p[i][j]) + "\n")

def main(argv):
    in_f = argv[1]
    n = int(argv[2])
    n_ = int(argv[3])
    out_d = argv[4]
    l = read_list(in_f)
    p = partition(l, n, n_)
    write_list(out_d, p)

    # print(json.dumps(p, indent=2))
    # print(json.dumps(p1, indent=2))

if __name__ == "__main__":
    main(sys.argv)

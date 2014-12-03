# Constructs the 30-topic sets from the 150 TREC 6, 7 and 8 topics.
# Usage: python tset.py
# Output is written to current directory

import sys, os
from random import *

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

def read_qid(f):
    l = open(f, "r").read().splitlines()
    l_ = []
    for i in range(len(l)):
        l_.append(int(l[i].split()[0]))
    return l_

def checks(s30):
    # checks
    print "sets"
    print "-------------------------"
    for i in range(len(s30)):
        print list(s30[i])

    print "union"
    print "-------------------------"
    s = s30[0] & s30[1] & s30[2] & s30[3] & s30[4]
    print s
    print len(s)

    print "intersection"
    print "-------------------------"
    s = list(s30[0] | s30[1] | s30[2] | s30[3] | s30[4])
    print s
    print len(s)
    
def init():
    home = os.environ["HOME"]
    # The ordering of elements in setlist is important, don't change
    # them. They map to elements of s30[] in order.
    setlist = ["301-450.fr.30",
               "301-450-fr.30",
               "301-450.a.30",
               "301-450.b.30",
               "301-450.c.30"]
    fr69 = read_qid(os.path.join(home, "ir/topic/fr94.69"))
    fr30 = read_qid(os.path.join(home, "ir/topic/fr94.30.no0"))
    t678 = read_qid(os.path.join(home, "ir/topic/301-450.150"))
    env  = {"setlist": setlist, "fr69": fr69, "t678": t678, "fr30": fr30}
    return env

def write_out_sets(s30, setlist):
    for i in range(len(setlist)):
        l = list(s30[i])
        with open(setlist[i], "w") as f:
            for i in range(len(l)):
                f.write(str(l[i]) + "\n")

# TREE3 layout of topic set construction
#
# Some FR topics have zero relevant docs, so the 30 fr topics were
# chosen so that they have at least 5 relevant documents. The rest of
# the 120 topics were randomly partitioned into sets of 30 as shown in
# the tree below.


          #             150
          #       --------------
          #      |              |
          #      69             81
          #  --------        --------
          # |        |      |        | 
          # 30       39     51       30
          # fr       |      |        301-450-fr
          # no 0      ------ 
          #              |
          #              90
          #         -----------
          #        |     |     |
          #        30    30    30
          #        a     b     c

def tree3(env):
    fr69 = env["fr69"]
    t678 = env["t678"]
    fr30 = env["fr30"]
    s30  = ["", "", "", "", ""]

    s150 = set(t678)
    s69  = set(fr69)
    
    s81 = s150 - s69

    #s30[0] = set(knuth_shuffle(list(s69))[:30])
    s30[0] = set(fr30)
    s39 = s69 - s30[0]

    s30[1] = set(knuth_shuffle(list(s81))[:30])
    s51 = s81 - s30[1]
    
    s90 = s39 | s51
    
    s30[2] = set(knuth_shuffle(list(s90))[:30])
    s60 = s90 - s30[2]

    s30[3] = set(knuth_shuffle(list(s60))[:30])
    s30[4] = s60 - s30[3]

    return s30

# layout of topic set construction

          #             150
          #       --------------
          #      |              |
          #      69             81
          #  --------        --------
          # |        |      |        | 
          # 30       39     51       30
          # fr       |      |        301-450-fr
          #           ------ 
          #              |
          #              90
          #         -----------
          #        |     |     |
          #        30    30    30
          #        a     b     c

def tree1(env):
    fr69 = env["fr69"]
    t678 = env["t678"]
    s30 = ["", "", "", "", ""]

    s150 = set(t678)
    s69 = set(fr69)
    
    s81 = s150 - s69

    s30[0] = set(knuth_shuffle(list(s69))[:30])
    s39 = s69 - s30[0]

    s30[1] = set(knuth_shuffle(list(s81))[:30])
    s51 = s81 - s30[1]
    
    s90 = s39 | s51
    
    s30[2] = set(knuth_shuffle(list(s90))[:30])
    s60 = s90 - s30[2]

    s30[3] = set(knuth_shuffle(list(s60))[:30])
    s30[4] = s60 - s30[3]

    return s30

# NOTE: tree2 is incorrect, because the 30 selected from the 120 to
# form the t678-cr-fr set may still contain an fr topic from the 39
# that went into the 120.

# layout of topic set construction

          #             150
          #       --------------
          #      |              |
          #      69             81
          #   -------           |
          #  |       |          |
          #  30      39         |
          #  fr      |          |
          #           ---------- 
          #              |
          #             120
          #  -------------------
          # |           |   |   |
          # 30          30  30  30
          # t678-cr-fr  a   b   c

def tree2(env):
    fr69 = env["fr69"]
    t678 = env["t678"]
    s30 = ["", "", "", "", ""]

    s150 = set(t678)
    s69 = set(fr69)
    
    s81 = s150 - s69

    s30[0] = set(knuth_shuffle(list(s69))[:30])
    s39 = s69 - s30[0]

    s120 = s39 | s81

    s30[1] = set(knuth_shuffle(list(s120))[:30])
    s90 = s120 - s30[1]

    s30[2] = set(knuth_shuffle(list(s90))[:30])
    s60 = s90 - s30[2]

    s30[3] = set(knuth_shuffle(list(s60))[:30])
    s30_5 = s60 - s30[3]


def main(argv):
    env = init()
    s30 = tree3(env)
    write_out_sets(s30, env["setlist"])

if __name__ == "__main__":
    main(sys.argv)
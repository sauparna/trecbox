import sys
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
    

fmap = ["../../../topics/fr94.qid",
        "../../../topics/t678-fr.qid",
        "../../../topics/t6.qid",
        "../../../topics/t7.qid",
        "../../../topics/t8.qid"]

def tree1():

    fr94 = read_qid("../../../topics/fr94.69.qid")
    t678 = read_qid("../../../topics/t678.qid")
    s30 = ["", "", "", "", ""]

    s150 = set(t678)
    s69 = set(fr94)
    
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

    for i in range(len(fmap)):
        l = list(s30[i])
        with open(fmap[i], "w") as f:
            for i in range(len(l)):
                f.write(str(l[i]) + "\n")
        
def tree2():

    fr94 = read_qid("../../../topics/fr94.69.qid")
    t678 = read_qid("../../../topics/t678.qid")
    s30 = ["", "", "", "", ""]

    s150 = set(t678)
    s69 = set(fr94)
    
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

    for i in range(len(fmap)):
        l = list(s30[i])
        with open(fmap[i], "w") as f:
            for i in range(len(l)):
                f.write(str(l[i]) + "\n")

def main(argv):
    tree1()

if __name__ == "__main__":
    main(sys.argv)

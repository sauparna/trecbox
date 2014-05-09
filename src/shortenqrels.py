# Read in a set of qids, and shorten a qrel to only those topics which
# are in this set.

import sys, os

def read_qid(f):
    l = open(f, "r").read().splitlines()
    l_ = []
    for i in range(len(l)):
        l_.append(int(l[i].split()[0]))
    return l_

def main(argv):
    home    = os.environ["HOME"]
    qid = {"ziff1":   read_qid(os.path.join(home, "ir/topics/ziff1.qid")),
           "ziff2":   read_qid(os.path.join(home, "ir/topics/ziff2.qid")),
           "fr94":    read_qid(os.path.join(home, "ir/topics/fr94.qid")),
           "t678-fr": read_qid(os.path.join(home, "ir/topics/t678-fr.qid")),
           "t6":      read_qid(os.path.join(home, "ir/topics/t6.qid")),
           "t7":      read_qid(os.path.join(home, "ir/topics/t7.qid")),
           "t8":      read_qid(os.path.join(home, "ir/topics/t8.qid"))}

    spin = ["|","/","-","|","-","\\"]

    l_t123 = open(os.path.join(home, "ir/qrels/qrels.1-150")).readlines()
    ziff1  = open(os.path.join(home, "ir/qrels/qrels.ziff1"), "w")
    ziff2  = open(os.path.join(home, "ir/qrels/qrels.ziff2"), "w")
    for i in range(len(l_t123)):
        print spin[i%5] + "\r",
        q = int(l_t123[i].split()[0])
        if q in qid["ziff1"]:
            ziff1.write(l_t123[i])
        if q in qid["ziff2"]:
            ziff2.write(l_t123[i])
    ziff2.close()
    ziff1.close()
    del(l_t123)

    l_t678  = open(os.path.join(home, "ir/qrels/qrels.301-450")).readlines()
    fr94    = open(os.path.join(home, "ir/qrels/qrels.fr94"), "w")
    t678_fr = open(os.path.join(home, "ir/qrels/qrels.t678-fr"), "w")
    t6      = open(os.path.join(home, "ir/qrels/qrels.t6"), "w")
    t7      = open(os.path.join(home, "ir/qrels/qrels.t7"), "w")
    t8      = open(os.path.join(home, "ir/qrels/qrels.t8"), "w")
    for i in range(len(l_t678)):
        print spin[i%5] + "\r",
        q = int(l_t678[i].split()[0])
        if q in qid["fr94"]:
            fr94.write(l_t678[i])
        if q in qid["t678-fr"]:
            t678_fr.write(l_t678[i])
        if q in qid["t6"]:
            t6.write(l_t678[i])
        if q in qid["t7"]:
            t7.write(l_t678[i])
        if q in qid["t8"]:
            t8.write(l_t678[i])
    t8.close()
    t7.close()
    t6.close()
    t678_fr.close()
    fr94.close()
    del(l_t678)

if __name__ == "__main__":
    main(sys.argv)

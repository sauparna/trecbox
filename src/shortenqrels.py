# Read in a set of qids, and shorten a qrel to only those topics which
# are in this set. This however shouldn't be necessary. If a query is
# not used for retrieval, eval doesn't see it at all, whether the query has
# relevance information in the qrel or not.

# Usage: python shortenqrels.py

import sys, os

def get_qid_list(f):
    l = open(f, "r").read().splitlines()
    l_ = []
    for i in range(len(l)):
        l_.append(int(l[i].split()[0]))
    return l_

def main(argv):
    home = os.environ["HOME"]
    qid = {"ziff1":   get_qid_list(os.path.join(home, "ir/topic/ziff1.30")),
           "ziff2":   get_qid_list(os.path.join(home, "ir/topic/ziff2.30")),
           "fr94":    get_qid_list(os.path.join(home, "ir/topic/fr94.30")),
           "t678-cr-fr": get_qid_list(os.path.join(home, "ir/topic/t678-cr-fr.30")),
           "t6":      get_qid_list(os.path.join(home, "ir/topic/t6.30")),
           "t7":      get_qid_list(os.path.join(home, "ir/topic/t7.30")),
           "t8":      get_qid_list(os.path.join(home, "ir/topic/t8.30"))}

    i_ziff  = open(os.path.join(home, "ir/qrel/1-100.cd12")).readlines()
    o_ziff1 = open(os.path.join(home, "ir/qrel/ziff1.cd12.30"), "w")
    o_ziff2 = open(os.path.join(home, "ir/qrel/ziff2.cd12.30"), "w")
    for i in range(len(i_ziff)):
        q = int(i_ziff[i].split()[0])
        if q in qid["ziff1"]:
            o_ziff1.write(i_ziff[i])
        if q in qid["ziff2"]:
            o_ziff2.write(i_ziff[i])
    o_ziff2.close()
    o_ziff1.close()
    del(i_ziff)

    i_t678 = open(os.path.join(home, "ir/qrel/301-450.cd45")).readlines()
    o_t6   = open(os.path.join(home, "ir/qrel/t6.cd45.30"), "w")
    for i in range(len(i_t678)):
        q = int(i_t678[i].split()[0])
        if q in qid["t6"]:
            o_t6.write(i_t678[i])
    o_t6.close()
    del(i_t678)

    i_t678_cr = open(os.path.join(home, "ir/qrel/301-450.cd45-cr")).readlines()
    o_fr94    = open(os.path.join(home, "ir/qrel/fr94.cd45-cr.30"), "w")
    o_t678_fr = open(os.path.join(home, "ir/qrel/t678-cr-fr.cd45.30"), "w")
    o_t7      = open(os.path.join(home, "ir/qrel/t7.cd45-cr.30"), "w")
    o_t8      = open(os.path.join(home, "ir/qrel/t8.cd45-cr.30"), "w")
    for i in range(len(i_t678_cr)):
        q = int(i_t678_cr[i].split()[0])
        if q in qid["fr94"]:
            o_fr94.write(i_t678_cr[i])
        if q in qid["t678-cr-fr"]:
            o_t678_fr.write(i_t678_cr[i])
        if q in qid["t7"]:
            o_t7.write(i_t678_cr[i])
        if q in qid["t8"]:
            o_t8.write(i_t678_cr[i])
    o_t8.close()
    o_t7.close()
    o_t678_fr.close()
    o_fr94.close()
    del(i_t678_cr)

if __name__ == "__main__":
    main(sys.argv)

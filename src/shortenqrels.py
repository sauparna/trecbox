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
    qid = {"ziff1": get_qid_list(os.path.join(home, "ir/topic/1-100.1.30")),
           "ziff2": get_qid_list(os.path.join(home, "ir/topic/1-100.2.30")),
           "t-fr" : get_qid_list(os.path.join(home, "ir/topic/301-450-fr.30")),
           "t.fr" : get_qid_list(os.path.join(home, "ir/topic/301-450.fr.30")),
           "t.a"  : get_qid_list(os.path.join(home, "ir/topic/301-450.a.30")),
           "t.b"  : get_qid_list(os.path.join(home, "ir/topic/301-450.b.30")),
           "t.c"  : get_qid_list(os.path.join(home, "ir/topic/301-450.c.30"))}

    i_ziff  = open(os.path.join(home, "ir/qrel/1-100.cd12")).readlines()

    o_ziff1 = open(os.path.join(home, "ir/qrel/1-100.1.cd12.30"), "w")
    o_ziff2 = open(os.path.join(home, "ir/qrel/1-100.2.cd12.30"), "w")
    for i in range(len(i_ziff)):
        q = int(i_ziff[i].split()[0])
        if q in qid["ziff1"]:
            o_ziff1.write(i_ziff[i])
        if q in qid["ziff2"]:
            o_ziff2.write(i_ziff[i])
    o_ziff2.close()
    o_ziff1.close()

    del(i_ziff)

    i_t678_cr_fr = open(os.path.join(home, "ir/qrel/301-450.cd45-cr-fr")).readlines()

    o_t678_fr = open(os.path.join(home, "ir/qrel/301-450-fr.cd45-cr-fr.30"), "w")
    for i in range(len(i_t678_cr_fr)):
        q = int(i_t678_cr_fr[i].split()[0])
        if q in qid["t-fr"]:
            o_t678_fr.write(i_t678_cr_fr[i])
    o_t678_fr.close()

    del(i_t678_cr_fr)

    i_t678_cr = open(os.path.join(home, "ir/qrel/301-450.cd45-cr")).readlines()

    o_fr      = open(os.path.join(home, "ir/qrel/301-450.fr.cd45-cr.30"), "w")
    o_a       = open(os.path.join(home, "ir/qrel/301-450.a.cd45-cr.30"), "w")
    o_b       = open(os.path.join(home, "ir/qrel/301-450.b.cd45-cr.30"), "w")
    o_c       = open(os.path.join(home, "ir/qrel/301-450.c.cd45-cr.30"), "w")
    for i in range(len(i_t678_cr)):
        q = int(i_t678_cr[i].split()[0])
        if q in qid["t.fr"]:
            o_fr.write(i_t678_cr[i])
        if q in qid["t.a"]:
            o_a.write(i_t678_cr[i])
        if q in qid["t.b"]:
            o_b.write(i_t678_cr[i])
        if q in qid["t.c"]:
            o_c.write(i_t678_cr[i])
    o_c.close()
    o_b.close()
    o_a.close()
    o_fr.close()

    del(i_t678_cr)

if __name__ == "__main__":
    main(sys.argv)

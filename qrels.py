# qrels stats, possibly plottable
# output is QID DOC1 DOC2 ...... total bin
# DOCi are acronyms for TREC document subsets
# total is the count of the total relevant (sum(DOCi))
# bin is a lable for the bin in which this fellow is
# bins are <= 5, 10, 50, 100 and > 100.
#
# Usage: qrels.py <qrels file>

import sys
from collections import OrderedDict as OD 
import os
import simplejson as json


# expected DOCNO prefixes from TREC 1-8 Adhoc test collections.
prefix = ["WS", "FR", "AP", "DO", "ZF", "SJ",
          "PT", "FT", "CR", "FB", "LA"]

def slurp(f):
    d = OD()
    with open(f, "r") as fp:
        for l in fp:
            qid, _, doc, rel = [a.rstrip().lstrip() for a in l.split()]
            qid = int(qid)
            rel = int(rel)
            dset = doc[:2]
            if dset not in prefix:
                print("Bad " + dset + "(" + doc + "), something wrong!")
                sys.exit(0)
            if qid not in d:
                d[qid] = OD()
            if dset not in d[qid]:
                d[qid][dset] = OD()
            d[qid][dset][doc] = rel
    return d

def count(d):
    d_ = OD()
    for qid in d:
        if qid not in d_:
            d_[qid] = OD()
        r = 0
        for dset in d[qid]:
            r_ = 0
            for doc in d[qid][dset]:
                r_ += d[qid][dset][doc]
            r += r_
            d_[qid][dset] = r_
        d_[qid]["total"] = r
        if r <= 5:
            d_[qid]["bin"] = 5
        elif r <= 10:
            d_[qid]["bin"] = 10
        elif r <= 50:
            d_[qid]["bin"] = 50
        elif r <= 100:
            d_[qid]["bin"] = 100
        else:
            d_[qid]["bin"] = -1
    return d_

def table(d, f=None):
    fp = None
    if f:
        fp = fopen(f, "w")
    pos    = {}
    fmt_   = "{:<6d}"
    fmt1_  = "{:<6}"
    fmt    = fmt_
    fmt1   = fmt1_
    header = ["QID"]
    
    # Bootstrap the header, the header format and the row
    # format. Though dicts are ordered, and qrels are sorted, the dset
    # strings are mapped to integers (pos) which would be used later
    # to index into a list (row) that holds the rel counts.

    for qid in d:
        i = 1 # Note that element 0 in header[] is already used.
        for dset in d[qid]:
            pos[dset] = i
            i += 1
            header.append(dset)
            fmt += fmt_
            fmt1 += fmt1_
        break
    
    print(fmt1.format(*header), file=fp)

    for qid in d:
        row = [0] * len(header)
        row[0] = qid
        for dset in d[qid]:
            row[pos[dset]] = d[qid][dset]
        print(fmt.format(*row), file=fp)
    if fp:
        fp.close()

def main(argv):
    # USAGE: qrels.py <qrels file>
    fi = argv[1]
    d  = slurp(fi)
    d_ = count(d)
    table(d_)

if __name__ == "__main__":
    main(sys.argv)

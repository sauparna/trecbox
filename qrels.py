# qrels stats, possibly plottable
# Usage: qrels.py <qrels file>

import sys
import collections
import os
import simplejson as json

# expected DOCNO prefixes from TREC 1-8 Adhoc test collections.
prefix = ["WS", "FR", "AP", "DO", "ZF", "SJ",
          "PT", "FT", "CR", "FB", "LA"]

def slurp(f):
    d = collections.OrderedDict()
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
                d[qid] = collections.OrderedDict()
            if dset not in d[qid]:
                d[qid][dset] = collections.OrderedDict()
            d[qid][dset][doc] = rel
    return d

def count(d):
    d_ = collections.OrderedDict()
    for qid in d:
        if qid not in d_:
            d_[qid] = collections.OrderedDict()
        r = 0
        for dset in d[qid]:
            r_ = 0
            for doc in d[qid][dset]:
                r_ += d[qid][dset][doc]
            r += r_
            d_[qid][dset] = r_
        d_[qid]["total"] = r
    return d_

def table(d):
    pos = {}
    fmt_ = "{:<6d}"
    fmt1_ = "{:<6}"
    fmt = fmt_
    fmt1 = fmt1_
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
    
    print(fmt1.format(*header))

    for qid in d:
        row = [0] * len(header)
        row[0] = qid
        for dset in d[qid]:
            row[pos[dset]] = d[qid][dset]
        print(fmt.format(*row))

def main(argv):
    # USAGE: qrels.py <qrels file>
    d = slurp(argv[1])
    d_ = count(d)
    table(d_)

if __name__ == "__main__":
    main(sys.argv)

# Reads the new kind of trec.offsets file, computes doc byte lengths
# and prints it out in this format:
#
# TESTCOL DOCNO BYTES
#
# NOTE: The lengths computed from the trec.offsets file is the length
# of the portion in TREC documents contained within the <TEXT> tag.
#
# USAGE: doclen trec.offsets outf

import sys
from collections import OrderedDict as OD
import simplejson as json
import numpy as NP

def slurp(f):
    d = OD({"FBIS":OD(), "FR":OD(), "FT":OD(), "LA":OD(), "T678":OD()})
    with open(f, "r") as fp:
        for l in fp:
            doc,cd_,_,lim_ = [x.strip() for x in l.split()]
            cd  = cd_.split("/")[0]
            b,e = [int(x) for x in lim_.split(":")]
            n   = e - b
            if n <= 0:
                n = 0
            if (cd == "cd4" or cd == "cd5") and not doc.startswith("CR"):
                d["T678"][doc] = n
                if doc.startswith("FBIS"):
                    d["FBIS"][doc] = n
                    continue
                if doc.startswith("FR"):
                    d["FR"][doc] = n
                    continue
                if doc.startswith("FT"):
                    d["FT"][doc] = n
                    continue
                if doc.startswith("LA"):
                    d["LA"][doc] = n
    return d

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    a = []
    for i in range(0, len(l), n):
        a.append(l[i:i+n])
    return a

def bin_bydocs(d, N=1000, f=None):
    # sort the docs by length, split them up into bins of 1000
    # documents, compute the median length in each bin.
    d_ = OD()
    for testcol in d:
        l = sorted(d[testcol].values())
        a = chunks(l, N) # list of lists
        v = []
        for i in range(len(a)):
            v.append(NP.median(a[i]))
        d_[testcol] = v
    return d_

def bin_bylengths(d, N=1000, f=None):
    # bin into N-byte ranges
    # in : d  = {testcol: {docno: len}}
    # out: d_ = {testcol: [n1, n2, ...]}
    # ni are the counts of the docs having length less than 1000*i
    d_ = OD()
    for testcol in d:
        l = [int(x) for x in d[testcol].values()]
        maxlen = NP.amax(l)
        nbins = int(maxlen / N) + 1
        v = [0] * nbins
        for i in range(len(l)):
            for j in range(nbins):
                lim = N * (j + 1)
                if l[i] < lim:
                    v[j] += 1
                    break
        d_[testcol] = v
    return d_

def print_bin_bylengths(d, N, f=None):
    # d = {testcol: [n1, n2, ...]}
    # ni is the count of the documents in bin i, of lenght less than N*i
    K = str(N / 1000)
    fp = None
    if f:
        f += "." + K + "K.lengths.bin"
        fp = open(f, "w")
    print("{} {} {}".format("testcol", "bin", "ndocs"), file=fp)
    for testcol in d:
        for i in range(len(d[testcol])):
            print("{} {} {}".format(testcol, i, d[testcol][i]), file=fp)
    if fp:
        fp.close()

def print_bin_bydocs(d, N, f=None):
    # d = {testcol: [n1, n2, ...]}
    # ni is the median byte length of documents in bin i
    K = str(N / 1000)
    fp = None
    if f:
        f += "." + K + "K.docs.bin"
        fp = open(f, "w")
    print("{} {} {}".format("testcol", "bin", "median"), file=fp)
    for testcol in d:
        for i in range(len(d[testcol])):
            print("{} {} {}".format(testcol, i, d[testcol][i]), file=fp)
    if fp:
        fp.close()

def print_stats(d, f=None):
    fp = None
    if f:
        f += ".stats"
        fp = open(f, "w")
    print("{:>10} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format("testcol", "ndocs", "mean", "median", "min", "max", "range"), file=fp)
    for testcol in d:
        v       = [int(x) for x in d[testcol].values()]
        _len    = len(v)
        _mean   = NP.mean(v)
        _median = NP.median(v)
        _min    = NP.amin(v)
        _max    = NP.amax(v)
        _range  = NP.ptp(v)
        print("{:>10} {:>10} {:>10.2f} {:>10.2f} {:>10d} {:>10d} {:>10d}".format(testcol, _len, _mean, _median, _min, _max, _range), file=fp)
    if fp:
        fp.close()

def print_doclens(d, f=None):
    fp = None
    if f:
        f += ".byte.len"
        fp = open(f, "w")
    print("{} {} {}".format("testcol", "docno", "bytes"), file=fp)
    for testcol in d:
        for doc in d[testcol]:
            print("{} {} {}".format(testcol, doc, d[testcol][doc]), file=fp)
    if fp:
        fp.close()

def main(argv):
    inf  = argv[1]
    outf = argv[2]

    d = slurp(inf)

    b = bin_bydocs(d, 1000)
    print_bin_bydocs(b, 1000, outf)

    b = bin_bylengths(d, 1000)
    print_bin_bylengths(b, 1000, outf)
    
    print_stats(d, outf)
    print_doclens(d, outf)

if __name__ == "__main__":
    main(sys.argv)

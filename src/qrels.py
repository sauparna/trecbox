# qrels stats, possibly plottable
# Usage: qrels.py <qrels file>
# Holds stuff in two dicts. The first has the entire list, the second the
# r and nr counts keyed by topic ID.

import sys
import collections
import fileinput
import os
import simplejson as json

# def build_dict(f):
#     d = collections.OrderedDict()
#     for l in fileinput.input(f):
#         f_ = os.path.basename(fileinput.filename())
#         a_ = [a__.rstrip().lstrip() for a__ in l.split()]
#         if f_ not in d:
#             d[f_] = collections.OrderedDict()
#         if a_[0] not in d[f_]:
#             d[f_][a_[0]] = collections.OrderedDict()
#         d[f_][a_[0]][a_[2]] = int(a_[3])
#     return d

def read_qrels(f):
    d = collections.OrderedDict()
    with open(f, "r") as fp:
        for l in fp:
            a_ = [a__.rstrip().lstrip() for a__ in l.split()]
            if a_[0] not in d:
                d[a_[0]] = {}
            d[a_[0]][a_[2]] = int(a_[3])
    return d

# def summarize(d):
#     d_ = collections.OrderedDict()
#     for f in d:
#         for q in d[f]:
            

def count_qrels(d):
    d_ = collections.OrderedDict()
    for q in d:
        if q not in d_:
            d_[q] = {}
        r = nr = 0
        for docno in d[q]:
            j = d[q][docno]
            if j == 0:
                nr += 1
            else:
                r+=1
        d_[q]["nr"] = nr
        d_[q]["r"] = r
    return d_

def print_rplot(d):
    fmt = "{} {} {}"
    print(fmt.format("id", "r", "nr"))
    for q in d:
        print(fmt.format(q, d[q]["r"], d[q]["nr"]))

def main(argv):
    d = read_qrels(argv[1])
    #d = build_dict(argv[1:])
    d_ = count_qrels(d)
    #print(json.dumps(d, indent=2))
    print_rplot(d_)

if __name__ == "__main__":
    main(sys.argv)

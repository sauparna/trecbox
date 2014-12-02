#!/usr/bin/env python3

# Given a set of TREC DOCNOs, bundle a corpus out of TREC CDs.
# input tuple [DOCNO, file, b1:b2, b3:b4, b5:b6]
#
# b_i pairs are DOC, DOCNO, TEXT offsets (in order)
#
# output is a file each for a TREC DOC, a 1000 thousand such in a
# folder.
#
# Usage: bundle.py trec.offsets <DOCNO list> <out dir>
#
# a is dict of DOCNOs
# b is TREC offsets file
# for each line in b
#     if DOCNO is in a
#         read DOC from TREC file
#         write DOC to new file

import sys
import simplejson as json
import os

def main(argv):

    if os.path.exists(argv[3]):
        print(argv[3] + " exists, quitting.")
        sys.exit()

    docno = {k: None for k in [l.rstrip() for l in open(argv[2], "r")]}
    d = {}

    c = 0
    with open(argv[1], "r") as fp:
        for l in fp:            
            a_ = [a__.rstrip().lstrip() for a__ in l.split()]
            if a_[0] in docno:
                c+=1; print(c, end="\r")
                if a_[1] not in d:
                    d[a_[1]] = {}
                if a_[0] not in d[a_[1]]:
                    d[a_[1]][a_[0]] = {}
                i = 2
                for k in ["DOC", "DOCNO", "TEXT"]:
                    d[a_[1]][a_[0]][k] = [int(x) for x in a_[i].split(":")]
                    i += 1
    print(str(c) + " DOCNOs read from master list")
    # print(json.dumps(d, indent=2))

    os.mkdir(argv[3])
    c = 0
    c_ = 0
    log  = open("log", "w")
    for f in d:
        #f_ = os.path.join(argv[3], os.path.basename(f))
        fp = open(f, "rb")
        #fp_ = open(f_, "wb")
        for g in d[f]:
            fp.seek(d[f][g]["DOC"][0])
            if c % 1000 == 0:
               c_ = int(c / 1000) 
               os.mkdir(os.path.join(argv[3], str(c_)))
            f_ = os.path.join(argv[3], str(c_), str(c))
            fp_ = open(f_, "wb")
            fp_.write(fp.read(d[f][g]["DOC"][1] - d[f][g]["DOC"][0] + 1))
            fp_.close()
            log.write(g + " " + f_ + " " + str(d[f][g]["DOC"][1] - d[f][g]["DOC"][0] + 1) + "\n")
            c+=1; print(c, end="\r")
        #fp_.close()
        fp.close()
    log.close()
    print(str(c) + " DOCs written, check inside '" + argv[3] + "'")

if __name__ == "__main__":
    main(sys.argv)

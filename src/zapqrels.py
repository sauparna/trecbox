#!/usr/bin/env python3

# Usage: zapqrels.py <full qrels file> <subset file> <out file>
import sys

def main(argv):
    docno = {k: None for k in [l.rstrip() for l in open(argv[2], "r")]}
    fp = open(argv[1], "r")
    fp_ = open(argv[3], "w")
    for l in fp:
        a = l.split()
        if a[2] in docno:
            fp_.write(l)
    fp_.close()
    fp.close()

if __name__ == "__main__":
    main(sys.argv)

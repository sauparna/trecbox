#!/usr/bin/env python3

# Usage: zapqrels.py <full qrels file> <subset file>
import sys

def main(argv):
    # docno = {k: None for k in [l.rstrip() for l in open(argv[2], "r")]}
    subset = {k: None for k in [l.rstrip() for l in open(argv[2], "r")]}
    with open(argv[1], "r") as fp:
        for l in fp:
            a = l.split()
            # if a[2] in docno:
            if a[0] in subset:
                print(l.strip())

if __name__ == "__main__":
    main(sys.argv)

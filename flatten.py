#!/usr/bin/env python3

# Flattens the TREC documents. It reads and writes out the entire TREC
# cd 1-5 corpus in neater format.
# Usage: flatten.py <TREC doc dir> <offsets file> <output dir>

import sys
import simplejson as json
import os
import uuid

def main(argv):
    d_in = argv[1]
    i_offsets = argv[2]
    d_out = argv[3]

    if os.path.exists(d_out):
        print(d_out + " output directory exists, quitting.")
        sys.exit()

    os.mkdir(d_out)

    c   = 0
    opened = ""
    i_fp = None
    o_fp = None
    pos = 0

    o_offsets = "/tmp/offsets." + str(uuid.uuid4())

    o_fp1 = open(o_offsets, "w")
    i_fp1 = open(i_offsets, "r")

    for l in i_fp1:

        print(c+1, end="\r")
        docno,fname,_,_,t = [l__.rstrip().lstrip() for l__ in l.split()]
        b,e = [int(n) for n in t.split(":")]

        if fname != opened:
            opened = fname
            pos = 0
            if i_fp:
                i_fp.close()
            i_f_ = os.path.join(d_in, fname)
            i_fp = open(i_f_, "rb")
            o_dir = os.path.join(d_out, os.path.dirname(fname))
            if not os.path.exists(o_dir):
                os.makedirs(o_dir)
            if o_fp:
                o_fp.close()
            o_f_ = os.path.join(d_out, fname)
            o_fp = open(o_f_, "wb")

        i_fp.seek(b)
        txt = bytearray(i_fp.read(e - b + 1))
        txt = txt.lstrip().rstrip()
        txt.append(10)

        sep = ("[[" + docno + "]]\n").encode()
        n = o_fp.write(sep)
        n1 = o_fp.write(txt)

        u = pos + 2; v = pos + n -  3 - 1
        x = pos + n; y = pos + n + n1 - 2
        o_str = docno + " " + fname + " " + str(u) + ":" + str(v) + " " + str(x) + ":"+ str(y) + "\n"
        o_fp1.write(o_str)
        pos += n + n1
        c += 1

    i_fp.close()
    o_fp.close()
    i_fp1.close()
    o_fp1.close()
    print(c)

if __name__ == "__main__":
    main(sys.argv)

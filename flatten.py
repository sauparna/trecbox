#!/usr/bin/env python3

# Flattens the TREC documents. It reads and writes out the entire TREC
# cd 1-5 corpus in neater format.
# Usage: flatten.py <TREC doc dir> <offsets file> <output dir>
import sys
import simplejson as json
import os

def main(argv):
    d_in = argv[1]
    f_offsets = argv[2]
    d_out = argv[3]

    if os.path.exists(d_out):
        print(d_out + " output directory exists, quitting.")
        sys.exit()

    os.mkdir(d_out)
    MAX = 10
    c   = 0
    c_  = 0
    od  = ""
    opened = ""
    i_fp = None

    i_fp1 = open(f_offsets, "r")
    for l in i_fp1:
        # print(c+1, end="\r")
        if (c % MAX) == 0:
            c_ = int(c / MAX)
            od = os.path.join(d_out, str(c_))
            print(od)
            os.mkdir(od)
        d,i_f,_,_,t = [l__.rstrip().lstrip() for l__ in l.split()]
        b,e = [int(n) for n in t.split(":")]

        if i_f != opened:
            opened = i_f
            if i_fp:
                i_fp.close()
            i_f_ = os.path.join(d_in, i_f)
            print(i_f_)
            i_fp = open(i_f_, "rb")
        i_fp.seek(b)
        txt = i_fp.read(e - b + 1)

        o_f = os.path.join(od, d)
        o_fp = open(o_f, "wb")
        o_fp.write(txt)
        o_fp.close()

        c += 1
    i_fp1.close()
    print(c)

if __name__ == "__main__":
    main(sys.argv)

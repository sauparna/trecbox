#!/usr/bin/env python3

# Folds the output of 'ggrep -Erob '<[\/]*(DOC|DOCNO|TEXT)[>]' cd12345/*'
# The grep output is [file name, byte offset, tag] tuples
#
# fold.py processes these tuples, to output: 
# [docno, file name, b1:b2, b3:b4, b5:b6], 
# where b_i pairs are the start and end byte offsets in a file.
#
# b1:b2 - marks a TREC document, the entire stuff starting from the
# '<' of the <DOC> tag and ending in '>' of the </DOC> tag.
#
# b3:b4 - the DOCNO, inside the <DOCNO> tags, adjusted for the
# presence of any whitespace between the tag boundaries and the DOCNO
# string
#
# b5:b6 - the content inside (and exlcuding) the <TEXT> tags.
#
# Usage: fold.py trec.grep 

import sys

def main(argv):
    old = new = None
    fmt = "{} {} {}:{} {}:{} {}:{}"
    with open(argv[1], "r") as fp:
        fp_ = None
        a = {}
        for l in fp:
            a_ = [a__.rstrip().lstrip() for a__ in l.split(":")]
            a[a_[2]] = int(a_[1])
            if a_[2] == "</DOC>":
                new = a_[0]
                if new != old:
                    if fp_:
                        fp_.close()
                    fp_ = open(new, "rb")
                    old = new
                b = a["<DOCNO>"] + 7
                e = a["</DOCNO>"] - 1
                fp_.seek(b)
                s__ = fp_.read(e-b+1)
                s__ = str(s__, encoding="UTF-8")
                s_ = s__.lstrip()
                s =  s_.rstrip()
                nl = len(s__) - len(s_)
                nr = len(s_) - len(s)
                l_ = fmt.format(s, a_[0], a["<DOC>"], a["</DOC>"]+6, a["<DOCNO>"]+7+nl, a["</DOCNO>"]-1-nr, a["<TEXT>"]+6, a["</TEXT>"]-1)
                print(l_)

if __name__ == "__main__":
    main(sys.argv)

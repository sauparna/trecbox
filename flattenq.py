# Flattens out TREC topics in my new format, writes the byte offsets
# in this new flattened file to another file in /tmp.
#
# NOTE: One old TREC topic set doesn't have 'd'
#
# TODO: Fix to handle topic files when missing 'd'

import sys, os
import uuid
import simplejson as json
from Topics import Topics

def main(argv):
    # USAGE: flattenq.py <TREC query file> <out file>
    f = argv[1]
    o = argv[2]
    t = Topics(f)
    qt = t.query(mode="t")
    qd = t.query(mode="d")
    qn = t.query(mode="n")

    # print(json.dumps(qt, indent=2))

    o_offsets = "/tmp/offsets." + str(uuid.uuid4())
    o_fp1 = open(o_offsets, "w")
    pos = 0
    fname = os.path.basename(f)

    with open(o, "wb") as o_fp:

        for i in qt:

            m = o_fp.write(("<TOP>\n").encode())

            pos += m

            x = o_fp.write(("<NUM>\n").encode())
            n = o_fp.write((str(i)).encode())
            y = o_fp.write(("\n</NUM>\n").encode())
            b = pos + x
            e = pos + x + n - 1
            stri = str(b) + ":" + str(e)

            pos += x + n + y

            x = o_fp.write(("<T>\n").encode())
            n = o_fp.write((qt[i]).encode())
            y = o_fp.write(("\n</T>\n").encode())
            b = pos + x
            e = pos + x + n - 1
            strt = str(b) + ":" + str(e)

            pos += x + n + y

            x = o_fp.write(("<D>\n").encode())
            n = o_fp.write((qd[i]).encode())
            y = o_fp.write(("\n</D>\n").encode())
            b = pos + x
            e = pos + x + n - 1
            strd = str(b) + ":" + str(e)

            pos += x + n + y

            x = o_fp.write(("<N>\n").encode())
            n = o_fp.write((qn[i]).encode())
            y = o_fp.write(("\n</N>\n").encode())
            b = pos + x
            e = pos + x + n - 1
            strn = str(b) + ":" + str(e)

            pos += x + n + y

            m = o_fp.write(("</TOP>\n").encode())

            pos += m

            o_str = " ".join([str(i), fname, stri, strt, strd, strn, "\n"])
            o_fp1.write(o_str)

    o_fp1.close()

if __name__ == "__main__":
    main(sys.argv)

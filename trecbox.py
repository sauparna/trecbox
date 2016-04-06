#!/usr/bin/env python3

import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri   import *
from SysLucene  import *
from Query      import Query

def init(x_f, y_f):

    x     = {}
    y     = {}
    y_str = os.path.basename(y_f)
    k_    = {"DOC"  : "doc",   "QUERY": "query",
             "QREL" : "qrel",  "MISC" : "misc",
             "INDEX": "index", "RUNS" : "runs",
             "EVALS": "evals", "LOG"  : "log"}

    with open(x_f, "r") as f:
              for l in f:
                  a = [a_.strip() for a_ in l.split()]
                  if a[0] == "" or a[0] == "#":
                      continue
                  x.update({a[0]: a[1]})

    x.update({k: os.path.join(x["EXP"], y_str, k_[k]) for k in k_})

    for k in k_:
        os.makedirs(x[k], exist_ok=True)

    with open(y_f, "r") as f:
              for l in f:
                  a = [a_.strip() for a_ in l.split()]
                  if a[0] == "" or a[0] == "#":
                      continue
                  if a[0] == "TESTCOL":
                      if a[0] in y:
                          y[a[0]].append(a[1:])
                      else:
                          y[a[0]] = [a[1:]]
                  else:
                      if a[0] in y:
                          y[a[0]].extend(a[1:])
                      else:
                          y[a[0]] = a[1:]

    return x, y

def maketag(docs, testcol, stop, stem, m, qnum, qtdn, qexp):
    
    stop_tag = {"ser17"        : "a",   "lucene33"  : "b",
                "indri418"     : "c",   "smart571"  : "d",
                "terrier733"   : "e",   ""          : "x"}

    stem_tag = {"porter"       : "p",   "weakporter": "w",
                "krovetz"      : "k",   "snowball"  : "o",
                "s"            : "s",   ""          : "x"}

    qexp_tag = {"kl"           : "kl0", "klapprox"  : "kla",
                "klinformation": "kli", "klcomplete": "klm", 
                "klcorrect"    : "klr", "bo1"       : "bo1", 
                "bo2"          : "bo2", ""          : "x"}

    if stop not in stop_tag:
        stop = ""
    if stem not in stem_tag:
        stem = ""
    if qexp not in qexp_tag:
        qexp = ""

    itag = docs    + "." + stop_tag[stop] + "." + stem_tag[stem]
    qtag = testcol + "." + qnum + "." + qtdn
    rtag = testcol + "." + stop_tag[stop] + "." + stem_tag[stem] + "." + m \
                   + "." + qnum + "." + qtdn + "." + qexp_tag[qexp]
    return itag, qtag, rtag

def main(argv):

    if len(argv) != 3:
        print("USAGE: python trecbox.py X Y")
        print("     : X = config file")
        print("     : Y = experiment map file")        
        sys.exit(0)

    x, y = init(argv[1], argv[2]);
    
    systems = {"terrier": SysTerrier(x), 
               "indri"  : SysIndri(x), 
               "lucene" : SysLucene(x)}
    
    system  = systems[y["SYS"][0]]

    c = 1

    for t in y["TESTCOL"]:

        d_dir     = os.path.join(x["DOC"], t[1])

        q         = t[2].split(":")
        q_f       = os.path.join(x["QUERY"], q[0])
        q_set     = []
        if len(q) == 3:
            q_set_f = os.path.join(x["QUERY"], q[2])
            q_set   = [int(l.strip()) for l in open(q_set_f, "r")]

        query = Query(q_f, q[1], q_set, y["SYS"][0])
        query.parse()
        _,q_tag,_ = maketag("", t[0], "", "",
                            "", str(query.n), q[1], "")
        query.write_xml(x["LOG"], q_tag + ".q")

        qrel_f = os.path.join(x["QREL"], t[3])

        for stop in y["STOP"]:

            stop_f = os.path.join(x["MISC"], stop)
            if stop == "x":
                stop   = ""
                stop_f = ""

            for stem in y["STEM"]:

                if stem == "x":
                    stem = ""

                itag,_,_ = maketag(t[1], "", stop, stem,
                                   "", "", "", "")
                print(itag)
                system.index(itag, d_dir, [stop_f, stem])

                for m in y["MODEL"]:
                    
                    m = m.split(":")
                    
                    for qexp in y["QEXP"]:

                        if qexp == "x":
                            qexp = ""

                        qexp = qexp.split(":")
                        _,_,rtag = maketag("", t[0], stop, stem, m[0],
                                           str(query.n), q[1], qexp[0])
                        print('{:<4} {}'.format(c, rtag))
                        system.retrieve(itag, rtag, [stop_f, stem],
                                        m, query.oqf, qexp)
                        system.evaluate(rtag, qrel_f)
                        c += 1

if __name__ == "__main__":
   main(sys.argv)

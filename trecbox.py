#!/usr/bin/env python3

import sys, os, time
import simplejson as json
from   SysTerrier import *
from   SysIndri   import *
from   SysLucene  import *
from   Query      import Query

def init(x_f, y_f):

    x = {}
    y = {}
    
    path, ext = os.path.splitext(y_f)
    if ext != ".txt":
        print("ERROR: Spec file extension must be '.txt'")
        sys.exit(0)
    y_str = os.path.basename(path)

    k_    = {"DOC"  : "doc",   "QUERY": "query",
             "QREL" : "qrel",  "MISC" : "misc",
             "INDEX": "index", "RUNS" : "runs",
             "EVALS": "evals", "LOG"  : "log"}

    with open(x_f, "r") as f:
              for l in f:
                  if (not l.strip()) or (l.strip() == "#"):
                      continue
                  a = [a_.strip() for a_ in l.split()]
                  x.update({a[0]: a[1]})

    x.update({k: os.path.join(x["EXP"], y_str, k_[k]) for k in k_})

    for k in k_:
        os.makedirs(x[k], exist_ok=True)

    with open(y_f, "r") as f:
              for l in f:
                  if (not l.strip()) or (l.strip() == "#"):
                      continue
                  a = [a_.strip() for a_ in l.split()]
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
    
    fp_stdout= open(os.path.join(x["LOG"], "stdout.txt"), "w")

    systems = {"terrier": SysTerrier(x),
               "indri"  : SysIndri(x), 
               "lucene" : SysLucene(x)}
    
    system  = systems[y["SYS"][0]]

    c, indexcount, retcount, evalcount = 1, 1, 1, 1
    indextime, rettime, evaltime = [], [], []

    n = len(y["TESTCOL"]) * len(y["MODEL"]) * len(y["STEM"]) \
        * len(y["STOP"])  * len(y["QEXP"])


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
            stop,_ = os.path.splitext(stop)
            if stop == "x":
                stop   = ""
                stop_f = ""

            for stem in y["STEM"]:

                if stem == "x":
                    stem = ""

                itag,_,_ = maketag(t[1], "", stop, stem,
                                   "", "", "", "")
                
                start = time.clock()
                system.index(itag, d_dir, [stop_f, stem])
                indextime.append((itag, time.clock() - start))
                str_stdout = '{:>5} {:<5} {:<30} {:<10}'.format(indexcount, ' ', itag, 
                      round(indextime[indexcount-1][1], 3))
                print(str_stdout)
                fp_stdout.write(str_stdout + '\n')
                indexcount += 1

                for m in y["MODEL"]:
                    
                    m = m.split(":")
                    
                    for qexp in y["QEXP"]:

                        if qexp == "x":
                            qexp = ""

                        qexp = qexp.split(":")
                        _,_,rtag = maketag("", t[0], stop, stem, m[0],
                                           str(query.n), q[1], qexp[0])

                        start = time.clock()
                        system.retrieve(itag, rtag, [stop_f, stem],
                                        m, query.oqf, qexp)
                        rettime.append((rtag, time.clock() - start))
                        
                        start = time.clock()
                        system.evaluate(rtag, qrel_f)
                        evaltime.append((rtag, time.clock() - start))
                        str_stdout = '{:>5}/{:<5} {:<30} {:<10} {:<10}'.format(c, n, rtag, 
                              round(rettime[c-1][1], 3), round(evaltime[c-1][1], 3))
                        print(str_stdout)
                        fp_stdout.write(str_stdout + '\n')
                        c += 1

    # Summarise the running times
    str_stdout = "Timings"
    print(str_stdout)
    fp_stdout.write(str_stdout + '\n')
    sum = 0.0
    for i in range(len(indextime)):
        sum += indextime[i][1]
        str_stdout = '{} took {:<.3f} seconds'.format(indextime[i][0], indextime[i][1])
        print(str_stdout)
        fp_stdout.write(str_stdout + '\n')
    str_stdout = '{:<5d} indexes took {:<.3f} seconds; {:<.3f} seconds on average.'.format(indexcount, sum, sum/len(indextime))
    print(str_stdout)
    fp_stdout.write(str_stdout + '\n')
    sum = 0.0
    for i in range(len(rettime)):
        sum += rettime[i][1]
    str_stdout = '{:<5d} retrieval runs took {:<.3f} seconds; {:<.3f} seconds on average.'.format(c, sum, sum/len(rettime))
    print(str_stdout)
    fp_stdout.write(str_stdout + '\n')
    sum = 0.0
    for i in range(len(evaltime)):
        sum += evaltime[i][1]
    str_stdout = '{:<5d} evaluations took {:<.3f} seconds; {:<.3f} seconds on average.'.format(c, sum, sum/len(evaltime))
    print(str_stdout)
    fp_stdout.write(str_stdout + '\n')

    fp_stdout.close()

if __name__ == "__main__":
   main(sys.argv)

#!/usr/bin/env python3

import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Query import Query

def read_config(x_f, y_f):
    y_str = os.path.basename(y_f)
    y     = json.loads(open(y_f, "r").read())
    x     = json.loads(open(x_f, "r").read())
    k_    = {"DOC"  : "doc",  "QUERY": "query", "QREL": "qrel",
             "MISC" : "misc", "INDEX": "index", "RUNS": "runs",
             "EVALS": "evals", "LOG": "log"}
    x.update({k: os.path.join(x["EXP"], y_str, k_[k]) for k in k_})
    return x, y

def maketag(docs, testcol, stop, stem, m, qnum, qtdn, qexp):
    stop_tag = {"ser17"     : "a",  "lucene33"  : "b",
                "indri418"  : "c",  "smart571"  : "d",
                "terrier733": "e",  ""          : "x"}
    stem_tag = {"porter"    : "p", "weakporter": "w", "krovetz": "k",
                "snowball"  : "o",          "s": "s",
                ""          : "x"}
    qexp_tag = {"kl"        : "kl0", "klapprox" : "kla", "klinformation":"kli",
                "klcomplete": "klm", "klcorrect": "klr",
                "bo1"       : "bo1", "bo2"      : "bo2", "": "x"}
    if stop not in stop_tag:
        stop = ""
    if stem not in stem_tag:
        stem = ""
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

    x, y = read_config(argv[1], argv[2]);
    
    systems = {"terrier": SysTerrier(x), 
               "indri"  : SysIndri(x), 
               "lucene" : SysLucene(x)}
    
    testcol     = y["testcol"]
    models      = y["models"]
    stops       = y["stops"]
    stems       = y["stems"]
    qexpansions = y["qexp"]
    system      = systems[y["system"]]

    c = 1

    for t in testcol:

        d_str     = testcol[t][0]
        d_d       = os.path.join(x["DOC"], d_str)
        q         = testcol[t][1].split(":")
        q_str     = q[0]
        q_f       = os.path.join(x["QUERY"], q_str)
        qrel_str  = testcol[t][2]
        qrel_f    = os.path.join(x["QREL"], qrel_str)
        q_tdn_str = q[1]
        q_set_str = None
        q_set_f   = None
        q_set     = []

        if len(q) == 3:
            q_set_str = q[2]
            q_set_f   = os.path.join(x["QUERY"], q_set_str)
            with open(q_set_f, "r") as fp:
                for l in fp:
                    q_set.append(int(l.strip()))
        
        query = Query(q_f, q_tdn_str, q_set, y["system"])
        query.parse()
        _,q_tag,_ = maketag("", t, "", "",
                           "", str(query.n), q_tdn_str, "")
        query.write_xml(x["RUNS"], q_tag + ".queries")
        
        for stop_str in stops:

            stop_f = os.path.join(x["MISC"], stop_str)
            if stop_str == "":
                stop_f   = ""
            
            for stem_str in stems:
                
                itag,_,_ = maketag(d_str, "", stop_str,
                                   stem_str, "", "", "", "")
                print(itag)
                system.index(itag, d_d, [stop_f, stem_str])

                for m_str in models:
                    
                    m = m_str.split(":")
                    
                    for qexp_str in qexpansions:

                        qexp = qexp_str.split(":")
                        _,_,rtag = maketag("", t, stop_str, stem_str, m[0],
                                           str(query.n), q_tdn_str, qexp[0])
                        print(str(c) + " " + rtag)
                        system.retrieve(itag, rtag, [stop_f, stem_str],
                                        m, query.oqf, qexp)
                        system.evaluate(rtag, qrel_f)
                        c += 1

if __name__ == "__main__":
   main(sys.argv)

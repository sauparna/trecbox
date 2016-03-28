#!/usr/bin/env python3

import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Query import Query

def init(cf, pf):
    name = os.path.basename(pf)
    plan = json.loads(open(pf, "r").read())
    path = json.loads(open(cf, "r").read())
    k_   = ["DOC", "QUERY", "QREL", "MISC", "INDEX", "RUNS", "EVALS"]
    path.update({k: os.path.join(path["EXP"], name, path[k]) for k in k_})
    return path, plan

def maketag(docs, testcol, stop, stem, m, qnum, qtdn, qe):
    itag = docs    + "." + stop + "." + stem
    qtag = testcol + "." + qnum + "." + qtdn
    rtag = testcol + "." + stop + "." + stem + "." + m \
                   + "." + qnum + "." + qtdn + "." + qe
    return itag, qtag, rtag

def main(argv):

    if len(argv) != 3:
        print("USAGE: python trecbox.py <conf file> <plan file>")
        sys.exit(0)

    stopmap = {"lucene33": "033", "indri418"  : "418",
               "smart571": "571", "terrier733": "733",
               "ser17"   : "017", "x"         : "x"}
    stemmap = {"porter"  : "po",  "weakporter": "wp", "krovetz": "kr",
               "snowball": "sn",          "s" : "s",
               "x"       : "x"}
    qemap   = {"kl": "kl0", "klapprox"  :"kla", "klinformation":"kli",
               "klcomplete":"klm", "klcorrect": "klr",
               "bo1":"bo1", "bo2":"bo2", "x": "x"}

    path, plan = init(argv[1], argv[2]);

    # # DEBUG
    # print(json.dumps(path, sort_keys=True, indent=2))
    # print(json.dumps(plan, sort_keys=True, indent=2))
    # sys.exit(0)

    systems = {"terrier": SysTerrier(path), 
               "indri"  : SysIndri(path), 
               "lucene" : SysLucene(path)}
    
    matrix = plan["matrix"]
    models = plan["models"]
    stops  = plan["stops"]
    stems  = plan["stems"]
    qexp   = plan["qexp"]
    system = systems[plan["system"]]

    c = 1

    for testcol in matrix:
        docs     = matrix[testcol][0]
        docsp    = os.path.join(path["DOC"], docs)
        q_       = matrix[testcol][1].split(":")
        queryf   = q_[0]
        queryp   = os.path.join(path["QUERY"], queryf)
        qrelsf   = matrix[testcol][2]
        qrelsp   = os.path.join(path["QREL"], qrelsf)
        qtdn     = q_[1]
        qsubsetf = None
        qsubsetp = None
        qsubsetl = []
        if len(q_) == 3:
            qsubsetf = q_[2]
            qsubsetp = os.path.join(path["QUERY"], qsubsetf)
            with open(qsubsetp, "r") as fp:
                for l in fp:
                    qsubsetl.append(int(l.strip()))
        query = Query(queryp, qtdn, qsubsetl, plan["system"])
        query.parse()
        _,qtag,_ = maketag("", testcol, "", "",
                           "", str(query.n), qtdn, "")
        query.write_xml(path["RUNS"], qtag + ".queries")
        for stopf in stops:
            if not stopf:
                stopf = "x"
            for stemmer in stems:
                if not stemmer:
                    stemmer = "x"
                itag,_,_ = maketag(docs, "", stopmap[stopf], stemmap[stemmer],
                                   "", "", "", "")
                print(itag)
                system.index(itag, docsp, [stopf, stemmap[stemmer]])
                for modstr in models:
                    model = modstr.split(":")
                    for qestr in qexp:
                        qe = qestr.split(":")
                        if not qe[0]:
                            qe[0] = "x"
                        _,_,rtag = maketag("", testcol, stopmap[stopf], stemmap[stemmer],
                                           model[0], str(query.n), qtdn, qemap[qe[0]])
                        print(str(c) + " " + rtag); c += 1 
                        system.retrieve(itag,  rtag, [stopf, stemmap[stemmer]], 
                                        model, query.oqf, qe)
                        system.evaluate(rtag, qrelsp)

if __name__ == "__main__":
   main(sys.argv)

import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def init(cf, pf):
    name = os.path.basename(pf)
    plan = json.loads(open(pf, "r").read())
    path = json.loads(open(cf, "r").read())
    k_   = ["DOCS", "TOPICS", "QRELS", "MISC", "INDEX", "RUNS", "EVALS"]
    path.update({k: os.path.join(path["EXP"], name, path[k]) for k in k_})
    return path, plan

def main(argv):

    if len(argv) != 3:
        print("USAGE: python trecbox.py <conf file> <plan file>")
        sys.exit(0)

    stopmap = {"lucene33": "033", "indri418"  : "418",
               "smart571": "571", "terrier733": "733",
               "x"       : "x"}
    stemmap = {"porter"  : "po",  "weakporter": "wp",
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

    for testcol in matrix:
        docs    = matrix[testcol][0]
        docsp   = os.path.join(path["DOCS"], docs)
        t_      = matrix[testcol][1].split(":")
        topicsf = t_[0]
        topicsp = os.path.join(path["TOPICS"], topicsf)
        qrelsf  = matrix[testcol][2]
        qrelsp  = os.path.join(path["QRELS"], qrelsf)
        
        qtdn     = t_[1]
        qsubsetf = None
        qsubsetp = None
        qsubsetl = []
        if len(t_) == 3:
            qsubsetf = t_[2]
            qsubsetp = os.path.join(path["TOPICS"], qsubsetf)
            with open(qsubsetp, "r") as fp:
                for l in fp:
                    qsubsetl.append(int(l.strip()))

        query = Topics(topicsp).query(plan["system"], qtdn, qsubsetl)
        qnum  = len(query)
        c = 1
        for stopf in stops:
            if not stopf:
                stopf = "x"
            for stemmer in stems:
                if not stemmer:
                    stemmer = "x"
                itag = docs + "." + stopmap[stopf] + "." + stemmap[stemmer]
                print(itag)
                system.index(itag, docsp, [stopf, stemmap[stemmer]])
                for modstr in models:
                    model = modstr.split(":")
                    for qestr in qexp:
                        qe = qestr.split(":")
                        if not qe[0]:
                            qe[0] = "x"
                        rtag = testcol + "." + stopmap[stopf] + "." + stemmap[stemmer] \
                                       + "." + model[0] \
                                       + "." + str(qnum) + "." + qtdn + "." + qemap[qe[0]]
                        print(str(c) + " " + rtag); c += 1 
                        system.retrieve(itag,  rtag, [stopf, stemmap[stemmer]], 
                                        model, query, qe)
                        system.evaluate(rtag, qrelsp)

if __name__ == "__main__":
   main(sys.argv)

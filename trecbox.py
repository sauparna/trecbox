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
    stems  = plan["stems"]
    system = systems[plan["system"]]

    for testcol in matrix:
        docs    = matrix[testcol][0]
        docsp   = os.path.join(path["DOCS"], docs)
        t_      = matrix[testcol][1].split(":")
        topicsf = t_[0]
        topicsp = os.path.join(path["TOPICS"], topicsf)
        qrelsf  = matrix[testcol][2]
        qrelsp  = os.path.join(path["QRELS"], qrelsf)
        
        part = "d"
        qsubsetf = None
        qsubsetp = None
        qsubsetl = None
        if len(t_) == 2:
            part = t_[1]
        if len(t_) == 3:
            qsubsetf = t_[2]
            qsubsetp = os.path.join(path["TOPICS"], qsubsetf)
            qsubsetl = list(set(open(qsubsetp, "r").read().splitlines()))

        query = Topics(topicsp).query(plan["system"], part, qsubsetl)
        for stemmer in stems:
            itag = docs + "." + stemmer
            print(itag)
            system.index(itag, docsp, ["stop", stemmer])
            for model in models:
                rtag = testcol + "." + stemmer + "." + model
                print(rtag)
                system.retrieve(itag,  rtag, ["stop", stemmer], model, query)
                system.evaluate(rtag, qrelsp)

if __name__ == "__main__":
   main(sys.argv)

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

    irsys_ = {"terrier": SysTerrier(path), 
              "indri"  : SysIndri(path), 
              "lucene" : SysLucene(path)}
    matrix = plan["matrix"]
    models = plan["models"]
    stems  = plan["stems"]
    irsys  = irsys_[plan["system"]]

    for i in matrix:
        d  = matrix[i][0]
        dp = os.path.join(path["DOCS"], d)
        t_ = matrix[i][1].split(":")
        tf = os.path.join(path["TOPICS"], t_[0])
        ql = None;
        if len(t_) == 3:
            qf = os.path.join(path["TOPICS"], t_[2])
            ql = list(set(open(qf, "r").read().splitlines()))
        q  = Topics(tf).query(plan["system"], t_[1], ql)
        qr = os.path.join(path["QRELS"], matrix[i][2])
        for s in stems:
            itag = d + "." + s
            print(itag)
            irsys.index(itag, dp, ["stop", s])
            for m in models:
                rtag = i + "." + s + "." + m
                print(rtag)
                irsys.retrieve(itag,  rtag, ["stop", s], m, q)
                irsys.evaluate(rtag, qr)

if __name__ == "__main__":
   main(sys.argv)

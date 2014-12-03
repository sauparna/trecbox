import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def init(cf, pf):
    # bootstrap paths
    # the name of the plan file will be the name of the output directory

    plan = json.loads(open(pf, "r").read())

    name = os.path.basename(pf)
    path = json.loads(open(cf, "r").read())
    i_exp = os.path.join(path["i_base"], path["in"]["exp"])
    if not os.path.exists(i_exp):
        print("Error: Experiment " + name + " doesn't exist in " + i_exp)
        print("Quitting.")
    
    for k in path["in"]:
        path["in"][k] = os.path.join(path["i_base"], path["in"][k])

    # overwrite
    path["in"]["topic"] = os.path.join(i_exp, name, "topics")
    path["in"]["qrel"]  = os.path.join(i_exp, name, "qrels")
    path["in"]["doc"]  = os.path.join(i_exp, name, "docs")

    path["o_base"] = os.path.join(path["o_base"], name)
    for k in path["out"]:
        path["out"][k] = os.path.join(path["o_base"], path["out"][k])
        if not os.path.exists(path["out"][k]):
            os.makedirs(path["out"][k])

    # flatten the path dict before passing it on to systems
    path.update(path["in"])
    path.update(path["out"])
    del(path["in"])
    del(path["out"])

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
        dp = os.path.join(path["doc"], d)
        t_ = matrix[i][1].split(":")
        tf = os.path.join(path["topic"], t_[0])
        ql = None;
        if len(t_) == 3:
            qf = os.path.join(path["topic"], t_[2])
            ql = list(set(open(qf, "r").read().splitlines()))
        q  = Topics(tf).query(plan["system"], t_[1], ql)
        qr = os.path.join(path["qrel"], matrix[i][2])
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
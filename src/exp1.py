import sys, os
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def init(config):
    path = []
    with open(config, "r") as f:
        path = f.readlines()
    home = path[0].rstrip("\n")
    out  = path[1].rstrip("\n")
    home_map = {"doc"     : "doc",
                "topics"  : "topics",
                "qrels"   : "qrels",
                "treceval": "trec_eval.9.0",
                "lucene"  : "lucene.TREC",
                "terrier" : "terrier-3.5",
                "indri"   : "indri-5.6",
                "utils"   : "utils"}
    out_map = {"index" : "index",
               "runs"  : "runs",
               "evals" : "evals",
               "attic" : "attic"}
    env = {}
    for k in home_map.keys():
        env[k] = os.path.join(home, home_map[k])
    for k in out_map.keys():
        env[k] = os.path.join(out, out_map[k])
    return env

def exp1(opt, env):

    # exp matrix, each row depicts:
    # runid: doc topic qrel
    matrix = {"t123": ["cd12", "51-200", "51-200.cd12"],
              "t4":   ["cd23", "201-250", "201-250.cd23"],
              "t5":   ["cd24", "251-300", "251-200.cd24"],
              "t678": ["cd45-cr", "301-450", "301-450.cd45-cr"]}

    models = ["bm25", "dfi0", "dirichletlm", "lemurtf_idf", "tf_idf"]
    stems  = ["n", "p"]

    s = SysTerrier(env)

    if opt == "i":
        doc = []
        for i in matrix.keys():
            d.append(matrix[i][0])
        doc = list(set(doc))
        for d in doc:
        d_path = os.path.join(env["doc"], d)
            for j in stems:
                s.index(d+"."+j,  d_path, ["stop", j])
    elif opt == "r":
        for i in matrix.keys():
            d = matrix[i][0]
            t_path = os.path.join(env["topic"], matrix[i][1])
            t = Topics(t_path)
            qid = open(t_path + ".qid", "r").read().splitlines()
            q = t.query("terrier", "d", qid)
            for j in stems:
                for k in models:
                    s.retrieve(d+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in matrix.keys():
            qrel = os.path.join(env["qrel"], matrix[i][2])
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrel)

def main(argv):
    if len(argv) != 2:
        print "usage: python setup.py <i|r|e>"
        sys.exit(0)

    env = init("config.exp1");

    if not (os.path.exists(env["index"]) 
            and os.path.exists(env["runs"]) 
            and os.path.exists(env["evals"])):
        print "Either one of index, runs or evals directory doesn't exist."
        sys.exit(0)

    exp1(argv[1], env)
    
if __name__ == "__main__":
   main(sys.argv)

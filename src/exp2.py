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
    models = ["bm25", "dfi0", "dirichletlm", "lemurtf_idf", "tf_idf"]
    stems  = ["n", "p"]

    doc    = {"fr94": os.path.join(env["doc"], "cd4/fr94"),
              "t678": os.path.join(env["doc"], "cd45-cr"),
              "t678-fr": os.path.join(env["doc"], "cd45-cr-fr"),
              "ziff": os.path.join(env["doc"], "ziff")}

    topics = {"t12": os.path.join(env["topics"], "t12.1-100"),
              "t6": os.path.join(env["topics"], "topics.301-350"),
              "t7": os.path.join(env["topics"], "topics.351-400"),
              "t8": os.path.join(env["topics"], "topics.401-450"),
              "t678": os.path.join(env["topics"], "topics.301-450")}

    qrels  = {"t12": os.path.join(env["qrels"], "t12.qrels.1-100.cd12"),
              "t6":   os.path.join(env["qrels"], "qrels.301-350.cd45"),
              "t7":   os.path.join(env["qrels"], "qrels.351-400.cd45-cr"),
              "t8":   os.path.join(env["qrels"], "qrels.401-450.cd45-cr"),
              "t678": os.path.join(env["qrels"], "t678.301-450.cd45-cr")}

    s = SysTerrier(env)
    # {"runid": "index topic qrel"}
    tag = {"fr94": "fr94 t678 t678",
           "t6": "t678 t6 t6",
           "t7": "t678 t7 t7",
           "t8": "t678 t8 t8",
           "t678": "t678 t678 t678",
           "t678-fr": "t678-fr t678 t678",
           "ziff": "ziff t12 t12"}
    if opt == "i":
        # pull out the index names
        a = []
        for i in tag.values():
            a.append(i.split()[0])
        index = list(set(a))
        for i in index:
            for j in stems:
                s.index(i+"."+j,  doc[i], ["stop", j])
    elif opt == "r":
        for i in tag.keys():
            i_ = tag[i].split()
            t = Topics(topics[i_[1]])
            qid = open(os.path.join(env["topics"],  i+".qid"), "r").read().splitlines()
            q = t.query("terrier", "d", qid)
            for j in stems:
                for k in models:
                    s.retrieve(i_[0]+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in tag.keys():
            i_ = tag[i].split()
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrels[i_[2]])

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

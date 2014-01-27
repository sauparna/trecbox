import sys, os
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

home = ""

# bootstrap env ('config' usually left out of version control)
with open("config", "r") as f:
    home = f.readline().rstrip("\n")

root = os.path.join(home, "exp")

env = {
    "doc"     : os.path.join(home, "doc"),
    "topics"  : os.path.join(home, "topics"),
    "qrels"   : os.path.join(home, "qrels"),
    "treceval": os.path.join(home, "trec_eval.9.0"),
    "lucene"  : os.path.join(home, "lucene.TREC"),
    "terrier" : os.path.join(home, "terrier-3.5"),
    "indri"   : os.path.join(home, "indri-5.6"),
    "utils"   : os.path.join(home, "utils"),
    "index"   : os.path.join(root, "index"),
    "runs"    : os.path.join(root, "runs"),
    "evals"   : os.path.join(root, "evals"),
    "attic"   : os.path.join(root, "attic")
    }

# dfrweightingmodel, idf don't work. See logs in w or attic
models = ["bb2","bm25","dfi0","dfr_bm25","dfree","dirichletlm",
          "dlh","dlh13","dph","hiemstra_lm","ifb2","in_expb2",
          "in_expc2","inb2","inl2","js_kls","lemurtf_idf",
          "lgd", "pl2", "tf_idf","xsqra_m"]

stems = ["n", "p", "s", "w"]

doc = {"t678": os.path.join(env["doc"], "trec678"),
       "t678-fr": os.path.join(env["doc"], "trec678-fr"),
       "fbis": os.path.join(env["doc"], "cd5/fbis"),
       "fr94": os.path.join(env["doc"], "cd4/fr94"),
       "ziff": os.path.join(env["doc"], "ziff")}

topics = {"t678": os.path.join(env["topics"], "topics.301-450"),
          "t6": os.path.join(env["topics"], "topics.301-350"),
          "t7": os.path.join(env["topics"], "topics.351-400"),
          "t8": os.path.join(env["topics"], "topics.401-450"),
          "ziff": os.path.join(env["topics"], "topics.1-150")}

qrels = {"t678": os.path.join(env["qrels"], "qrels.trec678.adhoc"),
         "t6": os.path.join(env["qrels"], "qrels.trec6.adhoc"),
         "t7": os.path.join(env["qrels"], "qrels.trec7.adhoc"),
         "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc"),
         "ziff": os.path.join(env["qrels"], "qrels.trec12.adhoc")}


def exp(opt):

    s = SysTerrier(env)
    
    tag = ["t6": "t678", "t7": "t678", "t8": "t678", 
           "t678-fr": "t678-fr", "fr94": "fr94", 
           "ziff1": "ziff", "ziff2": "ziff"]

    if opt == "i":
        for i in tag.values():
            for j in stems:
            s.index(i+"."+j,  doc[i], ["stop", j])
    elif opt == "r":
        for i in tag.keys():
            qid = open(os.path.join(env["topics"],  i+".qid"), "r").read().splitlines()
            t = Topics(tag[i])
            q = t.query("terrier", "d", qid)
            for j in stems:
                for k in models:
                    s.retrieve(tag[i]+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in tag.keys():
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrels[tag[i]])


def main(argv):
    if len(argv) != 2:
        print "usage: python setup.py <i|r|e>"
        sys.exit(0)

    if not (os.path.exists(env["index"]) 
            and os.path.exists(env["runs"]) 
            and os.path.exists(env["evals"])):
        print "Either of index, runs or evals directory doesn't exist."

    exp_ziff(argv[1])
    
if __name__ == "__main__":
   main(sys.argv)

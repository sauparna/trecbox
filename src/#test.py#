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
          "t123": os.path.join(env["topics"], "topics.1-150")}

qrels = {"t678": os.path.join(env["qrels"], "qrels.trec678.adhoc"),
         "t6": os.path.join(env["qrels"], "qrels.trec6.adhoc"),
         "t7": os.path.join(env["qrels"], "qrels.trec7.adhoc"),
         "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc"),
         "ziff": os.path.join(env["qrels"], "qrels.trec12.adhoc")}

def test1(opt):
    env = {
        "doc"     : os.path.join(home, "doc"),
        "topics"  : os.path.join(home, "topics"),
        "qrels"   : os.path.join(home, "qrels"),
        "treceval": os.path.join(home, "trec_eval.9.0"),
        "lucene"  : os.path.join(home, "lucene.TREC"),
        "terrier" : os.path.join(home, "terrier-3.5"),
        "indri"   : os.path.join(home, "indri-5.6"),
        "utils"   : os.path.join(home, "utils"),
        "index"   : os.path.join(root, "index.test1"),
        "runs"    : os.path.join(root, "runs.test1"),
        "evals"   : os.path.join(root, "evals.test1"),
        "attic"   : os.path.join(root, "attic")
        }
    
    doc = {"test1": os.path.join(env["doc"], "test1"),
           "t678": os.path.join(env["doc"], "trec678")}

    topics = {"test1": os.path.join(env["topics"], "topics.test1"),
              "t8": os.path.join(env["topics"], "topics.401-450")}

    qrels = {"test1": os.path.join(env["qrels"], "qrels.test1"),
             "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc")}

    models = ["tf_idf", "lemurtf_idf"]
    stems = ["n", "p"]

    # s = SysIndri(env)

    # s.index("test1b.n", doc["test1"], ["stop", "n"])
    # t = Topics(topics["test1"])
    # q = t.query("indri", "d")
    # s.retrieve("test1b.n", "test1b.n", q)
    # s.evaluate("test1b.n", qrels["test1"])

    # s.index("t678b.n", doc["t678"], ["stop", "n"])
    # s.index("t678b.p", doc["t678"], ["stop", "p"])
    # t = Topics(topics["t8"])
    # q = t.query("indri", "d")
    # s.retrieve("t678b.n", "t678b.n", q)
    # s.retrieve("t678b.p", "t678b.p", q)
    # s.evaluate("t678b.n", qrels["t8"])
    # s.evaluate("t678b.p", qrels["t8"])

    s = SysLucene(env)

    # s.index("test1c.n", doc["test1"], ["stop", "n"])
    # t = Topics(topics["test1"])
    # q = t.query("lucene", "d")
    # s.retrieve("test1c.n", "test1c.n", "bm25", q)
    # s.evaluate("test1c.n", qrels["test1"])

    # s.index("t678c.n", doc["t678"], ["stop", "n"])
    # s.index("t678c.p", doc["t678"], ["stop", "p"])

    t = Topics(topics["t8"])
    q = t.query("lucene", "d")
    s.retrieve("t678c.n", "t678c.n", "bm25", q)
    s.retrieve("t678c.p", "t678c.p", "bm25", q)
    s.evaluate("t678c.n", qrels["t8"])
    s.evaluate("t678c.p", qrels["t8"])

def test(opt):

    env = {
        "doc"     : os.path.join(home, "doc"),
        "topics"  : os.path.join(home, "topics"),
        "qrels"   : os.path.join(home, "qrels"),
        "treceval": os.path.join(home, "trec_eval.9.0"),
        "lucene"  : os.path.join(home, "lucene.TREC"),
        "terrier" : os.path.join(home, "terrier-3.5"),
        "indri"   : os.path.join(home, "indri-5.6"),
        "utils"   : os.path.join(home, "utils"),
        "index"   : os.path.join(root, "index.test1"),
        "runs"    : os.path.join(root, "runs.test1"),
        "evals"   : os.path.join(root, "evals.test1"),
        "attic"   : os.path.join(root, "attic")
        }
    
    doc = {"test1": os.path.join(env["doc"], "test1"),
           "t678a": os.path.join(env["doc"], "trec678")}

    topics = {"test1": os.path.join(env["topics"], "topics.test1"),
              "t8": os.path.join(env["topics"], "topics.401-450")}

    qrels = {"test1": os.path.join(env["qrels"], "qrels.test1"),
             "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc")}

    models = ["tf_idf", "lemurtf_idf"]
    stems = ["n", "p"]

    s = SysTerrier(env)
    # {"runid": "index topic qrel"}
    tag = {"t8": "t678 t8 t8"}
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
            q = t.query("terrier", "d")
            for j in stems:
                for k in models:
                    s.retrieve(i_[0]+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in tag.keys():
            i_ = tag[i].split()
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrels[i_[2]])


def exp1(opt):

    # t6,7,8 using 50 topics each

    models = ["bm25","dfree","dirichletlm",
              "lemurtf_idf","pl2", "tf_idf"]
    stems = ["n", "p"]

    s = SysTerrier(env)
    # {"runid": "index topic qrel"}
    tag = {"t6": "t678 t678 t6",
           "t7": "t678 t678 t7",
           "t8": "t678 t678 t8"}
    if opt == "i":
        print "Not indexing. Use existing ones."
        sys.exit(0)
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
            q = t.query("terrier", "d")
            for j in stems:
                for k in models:
                    s.retrieve(i_[0]+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in tag.keys():
            i_ = tag[i].split()
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrels[i_[2]])


def exp(opt):
    s = SysTerrier(env)
    # {"runid": "index topic qrel"}
    tag = {"t6": "t678 t678 t6",
           "t7": "t678 t678 t7",
           "t8": "t678 t678 t8",
           "t678-fr": "t678-fr t678 t678",
           "fr94": "fr94 t678 t678",
           "ziff1": "ziff t123 ziff",
           "ziff2": "ziff t123 ziff"}
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
    if not (os.path.exists(env["index"]) 
            and os.path.exists(env["runs"]) 
            and os.path.exists(env["evals"])):
        print "Either of index, runs or evals directory doesn't exist."
    #exp(argv[1])
    # exp1(argv[1])
    # test(argv[1])
    test1(argv[1])
    
if __name__ == "__main__":
   main(sys.argv)

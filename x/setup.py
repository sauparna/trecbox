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

models = ["bb2","bm25","dfi0","dfr_bm25","dfree","dfrweightingmodel",
          "dirichletlm","dlh","dlh13","dph","hiemstra_lm","idf",
          "ifb2","in_expb2","in_expc2","inb2","inl2","js_kls",
          "lemurtf_idf","lgd", "pl2", "tf_idf","xsqra_m"]

stemmers = ["porter", "weak-porter", "snowball"]

doc = {"t678": os.path.join(env["doc"], "trec678"),
       "t678-fr": os.path.join(env["doc"], "trec678-fr")}

topics = {"t678": os.path.join(env["topics"], "topics.301-450"),
          "t6": os.path.join(env["topics"], "topics.301-350"),
          "t7": os.path.join(env["topics"], "topics.331-400"),
          "t8": os.path.join(env["topics"], "topics.401-450")}

qrels = {"t678": os.path.join(env["qrels"], "qrels.trec678.adhoc"),
         "t6": os.path.join(env["qrels"], "qrels.trec6.adhoc"),
         "t7": os.path.join(env["qrels"], "qrels.trec7.adhoc"),
         "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc")}

def tests():
    qrels = {"test1": os.path.join(env["qrels"], "test1")}
    topic = {"test1": os.path.join(env["topics"], "test1")}
    doc = {"test" : os.path.join(env["doc"], "test")}
    t = Topics(topic["test1"])
    s = SysTerrier(env)
    #s.retrieve("xyz", "xyz", ["None", "None"], "tfidf", t.query("terrier"))
    #s.evaluate("xyz", qrels["test1"])

def exp_t678(opt):

    s = SysTerrier(env)

    if opt == "i":

        s.index("t678.n",  doc["t678"], ["stopwords", "None"])
        s.index("t678.p",  doc["t678"], ["stopwords", "porter"])
        s.index("t678.wp", doc["t678"], ["stopwords", "weak-porter"])
        s.index("t678.s",  doc["t678"], ["stopwords", "snowball"])

    elif opt == "r":

        t = Topics(topics["t678"], "d")
        q = t.query("terrier")

        for m in models:
            s.retrieve("t678.n",  "t678.n."  + m, ["stopwords", "None"],        m, q)
            s.retrieve("t678.p",  "t678.p."  + m, ["stopwords", "porter"],      m, q)
            s.retrieve("t678.wp", "t678.wp." + m, ["stopwords", "weak-porter"], m, q)
            s.retrieve("t678.s",  "t678.s."  + m, ["stopwords", "snowball"],    m, q)

    elif opt == "e":

        for m in models:
            s.evaluate("t678.n."  + m, qrels["t678"])
            s.evaluate("t678.p."  + m, qrels["t678"])
            s.evaluate("t678.wp." + m, qrels["t678"])
            s.evaluate("t678.s."  + m, qrels["t678"])

def exp_t678_fr(opt):

    s = SysTerrier(env)

    if opt == "i":

        s.index("t678-fr.n",  doc["t678-fr"], ["stopwords", "None"])
        s.index("t678-fr.p",  doc["t678-fr"], ["stopwords", "porter"])
        s.index("t678-fr.wp", doc["t678-fr"], ["stopwords", "weak-porter"])
        s.index("t678-fr.s",  doc["t678-fr"], ["stopwords", "snowball"])

    elif opt == "r":

        t = Topics(topics["t678"], "d")
        q = t.query("terrier")

        for m in models:
            s.retrieve("t678-fr",    "t678-fr."    + m, ["stopwords", "None"],        m, q)
            s.retrieve("t678-fr.p",  "t678-fr.p."  + m, ["stopwords", "porter"],      m, q)
            s.retrieve("t678-fr.wp", "t678-fr.wp." + m, ["stopwords", "weak-porter"], m, q)
            s.retrieve("t678-fr.s",  "t678-fr.s."  + m, ["stopwords", "snowball"],    m, q)

    elif opt == "e":

        for m in models:
            s.evaluate("t678-fr."    + m, qrels["t678"])
            s.evaluate("t678-fr.p."  + m, qrels["t678"])
            s.evaluate("t678-fr.wp." + m, qrels["t678"])
            s.evaluate("t678-fr.s."  + m, qrels["t678"])

# TODO
def exp_t6_7_8(opt):

    s = SysTerrier(env)

    if opt == "i":

        print "don't want to spend time indexing, use t678"

    elif opt == "r":

        for t in ["t6", "t7", "t8"]:

            t = Topics(topics["t6"], "d")
            q = t.query("terrier")

            for m in models:
                s.retrieve("t678",    "t6."    + m, ["stopwords", "None"],        m, q)
                s.retrieve("t678.p",  "t6.p."  + m, ["stopwords", "porter"],      m, q)
                s.retrieve("t678.wp", "t6.wp." + m, ["stopwords", "weak-porter"], m, q)
                s.retrieve("t678.s",  "t6.s."  + m, ["stopwords", "snowball"],    m, q)

    elif opt == "e":

        for m in models:
            s.evaluate("t6."    + m, qrels["t6"])
            s.evaluate("t6.p."  + m, qrels["t6"])
            s.evaluate("t6.wp." + m, qrels["t6"])
            s.evaluate("t6.s."  + m, qrels["t6"])


def main(argv):
    if len(argv) != 2:
        print "usage: python setup.py <i|r|e>"
        sys.exit(0)
    exp_t678(argv[1])
    
if __name__ == "__main__":
   main(sys.argv)

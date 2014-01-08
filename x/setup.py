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

models = ["bb2", "bm25", "dfr_bm25", "dlh", "dlh13", 
          "hiemstra_lm", "ifb2", "in_expb2", "in_expc2", 
          "inl2", "lemurtf_idf", "pl2", 
          "tf_idf", "pontecroft", "dfrweightingmodel"]

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

def exp(opt):
    t = Topics(topics["t678"], "d")
    s = SysTerrier(env)

    if opt == "i":
        s.index("t678", doc["t678"], ["stopwords", "None"])
        #s.index("t678.p", doc["t678"], ["stopwords", "porter"])
        #s.index("t678.wp", doc["t678"], ["stopwords", "weak-porter"])
        #s.index("t678.s", doc["t678"], ["stopwords", "snowball"])
    elif opt == "r":
        s.retrieve("t678", "t678.bm25", ["stopwords", "None"], "bm25", t.query("terrier"))
    elif opt == "e":
        s.evaluate("t678.bm25", qrels["t678"])

def main(argv):
    if len(argv) != 2:
        print "usage: python setup.py <i|r|e>"
        sys.exit(0)
    exp(argv[1])
    
if __name__ == "__main__":
   main(sys.argv)

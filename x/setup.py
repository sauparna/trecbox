import sys, os
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

home = "/home/palchowdhury/ir"
root = os.path.join(home, "exp")

env = {
    "doc"     : os.path.join(home, "doc"),
    "topics"  : os.path.join(home, "topics"),
    "qrels"   : os.path.join(home, "qrels"),
    "treceval": os.path.join(home, "trec_eval.9.0"),
    "lucene"  : os.path.join(home, "lucene.TREC"),
    "terrier" : os.path.join(home, "terrier-3.5"),
    "indri"   : os.path.join(home, "indri-5.6"),
    "utils"   : os.path.join(home, "utils")
    "index"   : os.path.join(root, "index"),
    "runs"    : os.path.join(root, "runs"),
    "evals"   : os.path.join(root, "evals"),
    "attic"   : os.path.join(root, "attic")
    }

doc   = {"test": os.path.join(env["doc"], "test"),
         "fbis": os.path.join(env["doc"], "cd45/fbis"),
         "fr94": os.path.join(env["doc"], "cd45/fr94"),
         "ft"  : os.path.join(env["doc"], "cd45/ft"),
         "la"  : os.path.join(env["doc"], "cd45/latimes")}

topic = {"t6": os.path.join(env["topics"], "topics.301-350"),
         "t7": os.path.join(env["topics"], "topics.351-400"),
         "t8": os.path.join(env["topics"], "topics.401-450")}

qrels = {"t6": os.path.join(env["qrels"], "qrels.trec6.adhoc.parts1-5"),
         "t7": os.path.join(env["qrels"], "qrels.trec7.adhoc.parts1-5"),
         "t8": os.path.join(env["qrels"], "qrels.trec8.adhoc.parts1-5")}

model = ["tfidf", "bm25"]

def main(argv):

    t = Topics(topic["t6"])

    #s = SysTerrier(env)
    s.index("xyz", doc["test"], ["stop", "porter"]])

    #s = SysIndri(env)
    #s.index("xyz", doc["test"], ["stop", "porter"]])

    #s = SysLucene(env)
    #s.index("xyz", doc["test"], ["stop", "porter"]])

    #s.retrieve("xyz", "xyz", "tfidf", t.query("lucene"))
    #s.retrieve("uvw", "uvw", "tfidf", t.query("indri"))
    #s.retrieve("rst", "rst", "tfidf", t.query("terrier"))
    #s.evaluate("rst", qrels["t6"])
    
if __name__ == "__main__":
   main(sys.argv[1:])

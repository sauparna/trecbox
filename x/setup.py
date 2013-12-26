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
    "index"   : os.path.join(root, "index"),
    "runs"    : os.path.join(root, "runs"),
    "evals"   : os.path.join(root, "evals")
    }

# systems are objects
# document collections are paths
# topics are objects
# qrels are files

#topic
# data:
#  topic - file
#  mode - type of query processing
#  query - constructs a query out of the topic
# func:
#  make_query()

doclist = [os.path.join(env["doc"], "test"),
           os.path.join(env["doc"], "cd45/fbis"),
           os.path.join(env["doc"], "cd45/fr94"),
           os.path.join(env["doc"], "cd45/ft")]

topiclist = [os.path.join(env["topics"], "topics.301-350"),
             os.path.join(env["topics"], "topics.351-400"),
             os.path.join(env["topics"], "topics.4010450")]

qrelslist = [os.path.join(env["qrels"], "qrels.trec6.adhoc.parts1-5"),
             os.path.join(env["qrels"], "qrels.trec7.adhoc.parts1-5"),
             os.path.join(env["qrels"], "qrels.trec8.adhoc.parts1-5")]

modellist = ["tfidf", "bm25"]

def main(argv):

    t = Topics(topiclist[0])
    #s = SysTerrier(env, d, t, m, qr)
    s = SysIndri(env)
    #s = SysLucene(env)
    #s.index(doclist[0], "uvw")
    #s.retrieve("xyz", "xyz", "tfidf", t.query("lucene"))
    #s.retrieve("uvw", "uvw", "tfidf", t.query("indri"))
    #s.retrieve("xyz", "xyz", "tfidf", t.query("terrier", "t"))
    s.evaluate("uvw", qrelslist[0])
    #s.evaluate("xyz", qrelslist[0])

    
if __name__ == "__main__":
   main(sys.argv[1:])

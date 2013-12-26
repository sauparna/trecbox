import sys, os
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

home = "/home/rup/ir/exp"

env = {
    "root": home,
    "doc": os.path.join(home, "doc"),
    "topics": os.path.join(home, "topics"),
    "qrels": os.path.join(home, "qrels"),
    "sys": os.path.join(home, "sys"),
    "index": os.path.join(home, "index"),
    "runs": os.path.join(home, "runs"),
    "evals": os.path.join(home, "eval"),
    "treceval": "/home/rup/trec_eval.9.0/trec_eval"
    # TODO: specify paths to systems too
}

# systems are objects
# document collections are paths
# topics are objects TODO: rethink
# qrels are files

#topic
# data:
#  topic - file
#  mode - type of query processing
#  query - file
# func:
#  make_query()

doclist = [
    os.path.join(env["doc"], "test"),
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

    t = Topics(topiclist[0], "t")

    #s = SysTerrier(env, d, t, m, qr)
    #s = SysIndri(env, d, t, m, qr)
    #s = SysLucene(env)
    #s.index(doclist[0], "xyz")
    #s.retrieve("xyz", "xyz", "tfidf", t.query_L())
    #s.retrieve("xyz", "xyz", "tfidf", t.query_I())
    #s.retrieve("xyz", "xyz", "tfidf", t.query_T(), "t")
    #s.evaluate("xyz", qrelslist[0])
    
if __name__ == "__main__":
   main(sys.argv[1:])

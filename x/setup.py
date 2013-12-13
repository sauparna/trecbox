import sys, os
from Sys import SysTerrier
from Doc import Doc
from Topics import Topics
from Qrels import Qrels
from Model import Model

home = "/home/rup/ir/exp"

env = {
    "root": home,
    "doc": os.path.join(home, "doc"),
    "topics": os.path.join(home, "topics"),
    "qrels": os.path.join(home, "qrels"),
    "sys": os.path.join(home, "sys"),
    "index": os.path.join(home, "index"),
    "runs": os.path.join(home, "runs"),
    "evals": os.path.join(home, "eval")
}

# systems are objects
# document collections are paths
# topics are objects
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

    d = Doc(doclist[0], "test")
    t = Topics(topiclist[0])
    m = Model(modellist[0])
    qr = Qrels(qrelslist[0])

    s = SysTerrier(env, d, t, m, qr)
    #s.index()
    #s.topic.build_query("t")
    #q = s.topic.query
    #s.retrieve(q)
    # s.evaluate()
    
if __name__ == "__main__":
   main(sys.argv[1:])

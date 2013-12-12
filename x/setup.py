import sys, os
from sys_ import sys_terrier
from doc_ import doc_
from topics_ import topics_
from qrels_ import qrels_
from model_ import model_

home = "/home/rup/ir/exp"

env = {
    "root": home,
    "doc": os.path.join(home, "doc"),
    "topics": os.path.join(home, "topics"),
    "qrels": os.path.join(home, "qrels"),
    "sys": os.path.join(home, "sys"),
    "index": os.path.join(home, "index"),
    "ret": os.path.join(home, "ret"),
    "eval": os.path.join(home, "eval")
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

modellist = ["A", "B"]

def main(argv):

    d = doc_(doclist[0], "test")
    t = topics_(topiclist[0])
    m = model_(modellist[0])
    qr = qrels_(qrelslist[0])

    s = sys_terrier(env, d, t, m, qr)
    s.index(d)
    # s.retrieve()
    # s.evaluate()
    
if __name__ == "__main__":
   main(sys.argv[1:])

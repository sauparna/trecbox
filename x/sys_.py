#system
# data:
#  doc - path
#  topic - topic object
#  query - file
#  qrel - file
#  index - path
#  rank list - file
#  score - file
# func:
#  query(topic, type-of-processing)
#  index(doc)
#  retrieve()
#  evaluate()

import os, subprocess

class sys_():
    def __init__(self):
        whoami = "base class"

class sys_terrier(sys_):

    # potential index ID candidates
    # sys name
    # doc

    # potential run ID candiates
    # sys name
    # doc
    # model
    # query
    
    def __init__(self, env, doc, topic, model, qrel):
        self.env = env
        self.doc = doc
        self.topic = topic
        self.qrel = qrel
        self.model = model
        self.param = {
            "terrier": "/home/rup/terrier-3.5/bin/trec_terrier.sh",
            "collection.spec": "-Dcollection.spec=" + os.path.join(env["index"], "doclist." + doc.name),
            # tune up index path name, create directory if necessary
            "terrier.index.path": "-Dterrier.index.path=" + env["index"],
            "trec.topics": "-Dtrec.topics=" + env["topics"],
            "trec.model": "-Dtrec.model=" + model.name
            }

    def index(self, doc):
        # create collection.spec
        # call terrier
        subprocess.check_output([self.param["terrier"], 
                                 "-i",
                                 self.param["collection.spec"],
                                 self.param["terrier.index.path"]])

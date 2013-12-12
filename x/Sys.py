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

class Sys():
    def __init__(self):
        whoami = "base class"

class SysTerrier(Sys):

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
            "doclist":  os.path.join(env["index"], "doclist." + doc.name),
            "index": os.path.join(env["index"], "t." + doc.name),
            "query": env["topics"], # may need more work
            "model": model.name
            }

    def index(self, doc):
        # create collection.spec

        # create index dir
        if os.path.exists(self.param["index"]):
            os.removedirs(self.param["index"])
        os.mkdir(self.param["index"])

        cmdargs = {
            "exec": "/home/rup/terrier-3.5/bin/trec_terrier.sh",
            "mode": "-i",
            "doclist": "-Dcollection.spec=" + self.param["doclist"],
            "index": "-Dterrier.index.path=" + self.param["index"]
            }

        # call terrier to index
        subprocess.check_output([cmdargs["exec"],
                                 cmdargs["mode"],
                                 cmdargs["doclist"],
                                 cmdargs["index"]])


        def retrieve(self, index, query):
            cmdargs = {
                "exec": "/home/rup/terrier-3.5/bin/trec_terrier.sh",
                "mode": "-r",
                "index": "-Dterrier.index.path=" + self.param["index"],
                "query": "-Dtrec.topics=" + self.param["query"],
                "model": "-Dtrec.model=" + self.param["model"]
                }

            # call terrier to retrieve
            subprocess.check_output([cmdargs["exec"], 
                                     cmdargs["mode"]])

            

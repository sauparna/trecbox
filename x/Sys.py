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

import os, subprocess, sys

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

    query_map = {"t": "TITLE", "d": "DESC", "n": "NARR"}
    model_map = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}

    def __init__(self, env, doc, topic, model, qrel):
        self.env = env
        self.doc = doc
        self.topic = topic
        self.qrel = qrel
        self.model = model
        
        self.param = {
            "doclist": os.path.join(env["index"], ".".join(["doclist", doc.name])),
            "index": os.path.join(env["index"], ".".join(["t", doc.name])),
            "topics": os.path.join(env["topics"], topic.file),
            "model": self.model_map[model.name],
            "runs": os.path.join(env["runs"], 
                                 ".".join(["t", doc.name, model.name, topic.query])),
            "evals": os.path.join(env["evals"], 
                                  ".".join(["t", doc.name, model.name, topic.query]))
            }

    def index(self):
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


    def retrieve(self, q):
        # create runs dir
        if os.path.exists(self.param["runs"]):
            os.removedirs(self.param["runs"])
        os.mkdir(self.param["runs"])

        # determine query
        l = list(self.topic.query)
        process = []
        skip = []
        for s in ["t", "d", "n"]:
            if s in l:
                process.append(self.query_map[s])
            else:
                skip.append(self.query_map[s])
        process = ",".join(process)
        skip = ",".join(skip)
        
        cmdargs = {
            "exec": "/home/rup/terrier-3.5/bin/trec_terrier.sh",
            "mode": "-r",
            "index": "-Dterrier.index.path=" + self.param["index"],
            "query": "-Dtrec.topics=" + self.param["topics"],
            "query1": "-DTrecQueryTags.doctag=TOP",
            "query2": "-DTrecQueryTags.process=TOP,NUM," + process,
            "query3": "-DTrecQueryTags.idtag=NUM",
            "query4": "-DTrecQueryTags.skip=" + skip,
            "query5": "-DTrecQueryTags.casesensitive=false",
            "model": "-Dtrec.model=" + self.param["model"],
            "runs": "-Dterrier.var=" + self.param["runs"]
            }
        
        # call terrier to retrieve
        subprocess.check_output([cmdargs["exec"], cmdargs["mode"], 
                                 cmdargs["index"], cmdargs["query"], 
                                 cmdargs["query1"], cmdargs["query2"], 
                                 cmdargs["query3"], cmdargs["query4"], 
                                 cmdargs["query5"], cmdargs["model"], 
                                 cmdargs["runs"]])

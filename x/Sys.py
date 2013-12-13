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
    def __init__(self, env, doc, topic, model, qrel):
        self.env = env
        self.doc = doc
        self.topic = topic
        self.qrel = qrel
        self.model = model
        
class SysTerrier(Sys):

    def __init__(self, env, doc, topic, model, qrel):
        Sys.__init__(self, env, doc, topic, model, qrel)
        self.sys_id = "T"
        self.index_id = ".".join([self.sys_id, self.doc.name])
        self.run_id = ".".join([self.sys_id, self.doc.name, 
                                self.model.name, self.topic.query])
        self.query_map = {"t": "TITLE", "d": "DESC", "n": "NARR"}
        self.model_map = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}
        self.param = {
            "doc": os.path.join(self.env["index"], 
                                ".".join(["doclist", self.doc.name])),
            "index": os.path.join(self.env["index"], self.index_id),
            "topics": os.path.join(self.env["topics"], self.topic.file),
            "model": self.model_map[model.name],
            "runs": os.path.join(self.env["runs"], self.run_id),
            "evals": os.path.join(self.env["evals"], self.run_id)
            }

    def index(self):
        # create collection.spec

        # create index dir
        # consider backing up an existing one with a stamp in stead of
        # deleting it

        if os.path.exists(self.param["index"]):
            os.removedirs(self.param["index"])
        os.mkdir(self.param["index"])

        args = {
            "exec": "/home/rup/terrier-3.5/bin/trec_terrier.sh",
            "mode": "-i",
            "doc": "-Dcollection.spec=" + self.param["doc"],
            "doc1": "-DTrecDocTags.doctag=DOC",
            "doc2": "-DTrecDocTags.idtag=DOCNO",
            "doc3": "-DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL",
            "doc4": "-DTrecDocTags.skip=DOCHDR",
            "index": "-Dterrier.index.path=" + self.param["index"]
            }

        # call terrier to index
        subprocess.check_output([args["exec"],
                                 args["mode"],
                                 args["doc"],
                                 args["index"]])

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
        
        args = {
            "exec": "/home/rup/terrier-3.5/bin/trec_terrier.sh",
            "mode": "-r",
            "index": "-Dterrier.index.path=" + self.param["index"],
            "query": "-Dtrec.topics=" + self.param["topics"],
            "query1": "-DTrecQueryTags.doctag=TOP",
            "query2": "-DTrecQueryTags.idtag=NUM",
            "query3": "-DTrecQueryTags.process=TOP,NUM," + process,
            "query4": "-DTrecQueryTags.skip=" + skip,
            "query5": "-DTrecQueryTags.casesensitive=false",
            "model": "-Dtrec.model=" + self.param["model"],
            #"runs": "-Dterrier.var=" + self.param["runs"]
            "runs": "-Dtrec.results.file" + self.param["runs"]
            }
        
        # call terrier to retrieve
        subprocess.check_output([args["exec"], args["mode"], 
                                 args["index"], args["query"], 
                                 args["query1"], args["query2"], 
                                 args["query3"], args["query4"], 
                                 args["query5"], args["model"], 
                                 args["runs"]])

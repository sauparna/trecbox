import sys
from Sys import *

class SysLucene(Sys):

    def __init__(self, env, doc, topic, model, qrel):
        Sys.__init__(self, env, doc, topic, model, qrel)
        self.sys_id = "L"
        self.index_id = ".".join([self.sys_id, self.doc.name])
        self.run_id = ".".join([self.sys_id, self.doc.name, 
                                self.model.name, self.topic.mode])
        self.model_map = {"bm25": "bm25", "dfr": "dfr", 
                          "tfidf": "default", "lm": "lm"}
        self.param = {
            "index": os.path.join(self.env["index"], self.index_id),
            "topics": os.path.join(self.env["topics"], self.topic.file),
            "runs": os.path.join(self.env["runs"], self.run_id),
            "model": self.model_map[model.name],
            "evals": os.path.join(self.env["evals"], self.run_id)
            }

    def index(self):

        # consider backing up an existing one with a stamp instead of
        # deleting it
        #if os.path.exists(self.param["index"]):
        #    os.removedirs(self.param["index"])
        #os.mkdir(self.param["index"])

        #java -cp "lucene.TREC/lib/*:lucene.TREC/bin/lucene.TREC.jar" IndexTREC 
        #-docs lucene.TREC/src

        jar = "/home/rup/lucene.TREC/bin/lucene.TREC.jar"
        lib = "/home/rup/lucene.TREC/lib/*"

        args = {
            "exec": "java",
            "cp": "-cp" ,
            "cp1": jar + ":" + lib,
            "bin": "IndexTREC",
            "index": "-index",
            "index1": self.param["index"],
            "doc": "-docs",
            "doc1": self.doc.path
            }

        subprocess.check_output([args["exec"], args["cp"], args["cp1"],
                                 args["bin"], args["index"], args["index1"],
                                 args["doc"], args["doc1"]])

    def retrieve(self):
        
        # determine query
        # query here is a dict
        
        #java -cp "bin:lib/*" BatchSearch -index /path/to/index 
        #-queries /path/to/title-queries.301-450 -simfn default > default.out

        jar = "/home/rup/lucene.TREC/bin/lucene.TREC.jar"
        lib = "/home/rup/lucene.TREC/lib/*"

        args = {
            "exec": "java",
            "cp": "-cp",
            "cp1": jar + ":" + lib,
            "bin": "BatchSearch",
            "index": "-index",
            "index1": self.param["index"],
            # For now, pass Ian's topic file
            # TODO: figure out format and introduce a query construct
            "query": "-queries",
            #"query1": self.topic.file,
            "query1":  "/home/rup/lucene.TREC/test-data/title-queries.301-450",
            "model": "-simfn",
            "model1": self.param["model"]
            }

        with open(self.param["runs"], "w") as f:
            f.write(subprocess.check_output([args["exec"], 
                                             args["cp"], args["cp1"],
                                             args["bin"], 
                                             args["index"], args["index1"],
                                             args["query"], args["query1"],
                                             args["model"], args["model1"]]))

    def evaluate(self):

        # overwrites files in eval dir
        
        args = {
            "exec": self.env["treceval"],
            "mode": "-q",
            "qrel": self.qrel.file,
            "run": self.param["runs"]
            }

        # trec_eval -q QREL_file Retrieval_Results > eval_output
        # call trec_eval and dump output to a file

        with open(self.param["evals"], "w") as f:
            f.write(subprocess.check_output([args["exec"], args["mode"],
                                             args["qrel"], args["run"]]))

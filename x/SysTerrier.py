from Sys import *

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
        # TODO: create collection.spec
        # do something about this step, very irritating indeed

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
            "doc5": "-DTrecDocTags.casesensitive=true",
            "index": "-Dterrier.index.path=" + self.param["index"]
            }

        # call terrier to index
        subprocess.check_output([args.pop("exec"), args.pop("mode")] 
                                + args.values())

    def retrieve(self):

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
            "rundir": "-Dtrec.results=" + self.env["runs"],
            "runfile": "-Dtrec.results.file=" + self.run_id
            }
        
        # call terrier to retrieve
        subprocess.check_output([args.pop("exec"), args.pop("mode")] 
                                + args.values())

    def evaluate(self):

        # overwrites files in eval dir
        # trec_eval -q QREL_file Retrieval_Results > eval_output
        
        args = {
            "exec": self.env["treceval"],
            "mode": "-q",
            "qrel": self.qrel.file,
            "runfile": os.path.join(self.param["runs"])
            }

        # call trec_eval and dump output to a file
        with open(self.param["evals"], "w") as f:
            f.write(subprocess.check_output([args["exec"], args["mode"],
                                             args["qrel"], args["runfile"]]))

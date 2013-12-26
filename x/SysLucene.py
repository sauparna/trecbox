import sys

class SysLucene():

    def __init__(self, env):
        self.env = env
        self.model_map = {"bm25": "bm25", "dfr": "dfr", 
                          "tfidf": "default", "lm": "lm"}

    def index(self, doc, itag):

        o_dir = os.path.join(self.env["index"], itag)
        jar = "/home/rup/lucene.TREC/bin/lucene.TREC.jar"
        lib = "/home/rup/lucene.TREC/lib/*"

        if os.path.exists(o_dir):
            os.removedirs(o_dir)
        
        #java -cp "lucene.TREC/lib/*:lucene.TREC/bin/lucene.TREC.jar" IndexTREC 
        #-docs lucene.TREC/src

        subprocess.check_output(["java",
                                 "-cp", jar + ":" + lib,
                                 "IndexTREC",
                                 "-index", o_dir,
                                 "-docs", doc
                                 ])

    def retrieve(self, itag, rtag, m, q):

        i_dir = os.path.join(self.env["index"], itag)
        o_file = os.path.join(self.env["runs"], rtag)
        jar = "/home/rup/lucene.TREC/bin/lucene.TREC.jar"
        lib = "/home/rup/lucene.TREC/lib/*"

        #java -cp "bin:lib/*" BatchSearch -index /path/to/index 
        #-queries /path/to/title-queries.301-450 -simfn default > default.out

        with open(o_file, "w") as f:
            f.write(
                subprocess.check_output(
                    ["java",
                     "-cp", jar + ":" + lib,
                     "BatchSearch",
                     "-index", i_dir,
                     "-queries", q,
                     "-simfn", self.model_map[m]]
                    )
                )

    def evaluate(self, rtag, qrels):

        # overwrites files in eval dir

        # check for rtag and qrels
        
        # trec_eval -q QREL_file Retrieval_Results > eval_output
        # call trec_eval and dump output to a file

        i_file = os.path.join(self.env["runs"], rtag)
        o_file = os.path.join(self.env["evals"], rtag)

        with open(o_file, "w") as f:
            f.write(subprocess.check_output([self.env["treceval"],
                                             "-q", 
                                             qrels,
                                             i_file]))

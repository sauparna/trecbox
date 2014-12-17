import sys, os, subprocess

class SysLucene():

    def __init__(self, path):
        self.path = path
        self.model_map   = {"bm25": "bm25", "dfr": "dfr", 
                            "tf_idf": "default", "lm": "lm"}
        self.stemmer_map = {"p": "porter", "k": "krovetz", 
                            "s": "snowball", "s1": "sstemmer"}
        self.jar = os.path.join(self.path["LUCENE"], "bin/lucene.TREC.jar")
        self.lib = os.path.join(self.path["LUCENE"], "lib/*")


    def __query_file(self, rtag, q):

        o_file = os.path.join(self.path["RUNS"], ".".join([rtag, "lucene"]))

        with open(o_file, "w") as f:
            for num in q.keys():
                f.write(num + " " + q[num] + "\n")

        return o_file


    def index(self, itag, doc, opt):
        
        # print(itag)

        stemmer = ""
        stopwords = ""

        if opt[0] != "None":
            stopwords = os.path.join(self.path["MISC"], opt[0])

        if opt[1] in self.stemmer_map.keys():
            stemmer = self.stemmer_map[opt[1]]

        o_dir = os.path.join(self.path["INDEX"], itag)

        if os.path.exists(o_dir):
            print("index(): found, so skipping " + itag)
            return

        #java -cp "lucene.TREC/lib/*:lucene.TREC/bin/lucene.TREC.jar" IndexTREC 
        #-docs lucene.TREC/src

        log = ""

        try:
            log = subprocess.check_output(["java",
                                           "-Xmx1024m",
                                           "-cp", self.jar + ":" + self.lib,
                                           "IndexTREC",
                                           "-index", o_dir,
                                           "-docs", doc,
                                           "-stop", stopwords,
                                           "-stem", stemmer],
                                          stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            log = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)

        o_log = os.path.join(os.path.join(self.path["INDEX"], itag + ".log"))
        with open(o_log, "w+b") as f:
            f.write(log)


    def retrieve(self, itag, rtag, opt, m, q):

        # NOTE: Unused parameter 'opt'. Kept to maintain parity with other system retrieve() calls.

        # print(rtag)

        i_dir = os.path.join(self.path["INDEX"], itag)
        i_file = self.__query_file(rtag, q)
        o_file = os.path.join(self.path["RUNS"], rtag)
        log = ""

        if not os.path.exists(i_dir):
            print("retrieve(): didn't find index " + itag)
            return

        if os.path.exists(os.path.join(o_file)):
            print("retrieve(): found, so skipping " + rtag)
            return

        #java -cp "bin:lib/*" BatchSearch -index /path/to/index 
        #-queries /path/to/title-queries.301-450 -simfn default > default.out

        with open(o_file, "w+b") as f:
            f.write(
                subprocess.check_output(
                    ["java",
                     "-cp", self.jar + ":" + self.lib,
                     "BatchSearch",
                     "-index", i_dir,
                     "-queries", i_file,
                     "-simfn", self.model_map[m]]
                    )
                )


    def evaluate(self, rtag, qrels):

        # print(rtag)

        # trec_eval -q QREL_file Retrieval_Results > eval_output
        # call trec_eval and dump output to a file

        i_file = os.path.join(self.path["RUNS"], rtag)
        o_file = os.path.join(self.path["EVALS"], rtag)

        if not os.path.exists(i_file):
            print("evaluate(): didn't find run " + rtag)
            return

        if os.path.exists(o_file):
            print("evaluate(): found, so skipping " + rtag)
            return

        with open(o_file, "w+b") as f:
            f.write(subprocess.check_output(
                    [os.path.join(self.path["TRECEVAL"], "trec_eval"),
                     "-q", 
                     qrels,
                     i_file]))

import sys, os, subprocess
from bs4 import BeautifulSoup

class SysLucene():

    def __init__(self, x):
        self.x         = x
        self.model_f   = os.path.join(self.x["LUCENE"], "models")
        self.model_map = {}

        with open(self.model_f, "r") as f:
              for l in f:
                  a = [a_.strip() for a_ in l.split()]
                  if a[0] == "" or a[0] == "#":
                      continue
                  self.model_map.update({a[0]: a[1]})

        self.stemmer_map = {"porter"  : "PorterStemFilter",
                            "krovetz" : "KStemFilter", 
                            "snowball": "SnowballFilter",
                            "s"       : "EnglishMinimalStemFilter"}
        self.lib         = os.path.join(self.x["LUCENE"], "lib/*")

    def index(self, itag, doc, opt):
        
        # print(itag)

        stop_f  = "None"
        stemmer = "None"
        if opt[0] != "":
            stop_f = opt[0]
        if opt[1] in self.stemmer_map:
            stemmer = self.stemmer_map[opt[1]]

        o_dir = os.path.join(self.x["INDEX"], itag)

        if os.path.exists(o_dir):
            print("WARN: Skipped stage, perhaps index exists in " + o_dir)
            return

        #java -cp "lucene-5.3.1/trec/lib/*:lucene-5.3.2/trec/bin/TREC.jar" IndexTREC 
        #-docs doc/

        output = ""
        
        try:
            output = subprocess.check_output(["java",
                                           "-Xmx2048m",
                                           "-cp",       self.lib,
                                           "IndexTREC",
                                           "-index",    o_dir,
                                           "-docs",     doc,
                                           "-stop",     stop_f,
                                           "-stem",     stemmer],
                                          stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)

        o_log = os.path.join(os.path.join(self.x["LOG"], itag + ".i"))
        with open(o_log, "w+") as f:
            f.write(str(output))


    def retrieve(self, itag, rtag, opt, m, q, qe):

        # NOTE: Unused parameters 'opt' and 'qe'. Kept to maintain
        # parity with other system retrieve() calls. I haven't figured
        # out how to do query-expansion in Lucene.

        # print(rtag)

        stop_f  = "None"
        stemmer = "None"
        if opt[0] != "":
            stop_f = opt[0]
        if opt[1] in self.stemmer_map:
            stemmer = self.stemmer_map[opt[1]]
        
        i_dir  = os.path.join(self.x["INDEX"], itag)
        i_file = q
        o_file = os.path.join(self.x["RUNS"], rtag)

        if not os.path.exists(i_dir):
            print("WARN: Couldn't retrieve, missing index " + i_dir)
            return
        if os.path.exists(os.path.join(o_file)):
            print("WARN: Skipped stage, run exists " + o_file)
            return

        #java -cp "bin:lib/*" BatchSearch -index /path/to/index 
        #-queries /path/to/queryfile -simfn default > default.out

        output = ""
        
        try:
            output = subprocess.check_output(
                        ["java",
                         "-cp",         self.lib,
                         "BatchSearch",
                         "-index",      i_dir,
                         "-queries",    i_file,
                         "-similarity", self.model_map[m[0]],
                         "-stop",       stop_f,
                         "-stem",       stemmer
                        ]
                    )
            with open(o_file, "w+b") as f:
                f.write(output)
        except subprocess.CalledProcessError as e:
            output = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)
            o_log = os.path.join(os.path.join(self.x["LOG"], rtag + ".r"))
            with open(o_log, "w+") as f:
                f.write(str(output))


    def evaluate(self, rtag, qrels):

        # print(rtag)

        i_file = os.path.join(self.x["RUNS"], rtag)
        o_file = os.path.join(self.x["EVALS"], rtag)
        output = ""

        if not os.path.exists(i_file):
            print("WARN: Couldn't eval, missing run " + i_file)
            return
        if os.path.exists(o_file):
            print("WARN: Skipped stage, eval exists " + o_file)
            return
        
        # trec_eval -q qrels run > eval_output
        try:
            output = subprocess.check_output(
                [os.path.join(self.x["EVAL"], "trec_eval"),
                 "-q", 
                 qrels,
                 i_file])
            with open(o_file, "w+b") as f:
                f.write(output)
        except subprocess.CalledProcessError as e:
            output = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)
            o_log = os.path.join(os.path.join(self.x["LOG"], rtag + ".e"))
            with open(o_log, "w+") as f:
                f.write(str(output))

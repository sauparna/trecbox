import sys, os, subprocess
import time

class SysTerrier():


    def __init__(self, env):

        self.env = env
        self.query_map   = {"t": "TITLE", "d": "DESC", "n": "NARR"}
        self.model_map   = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}
        self.stemmer_map = {"porter": "PorterStemmer", "weak-porter": "WeakPorterStemmer", "snowball": "EnglishSnowballStemmer"}
        self.stopfile    = "stop"


    def __write_doclist(itag):

        # write Terrier's collection.spec file
        o_file = os.path.join(self.env["index"], ".".join([itag, "terrier"]))

        with open(o_file, "w") as f:
            f.write(subprocess.check_output(["find", doc, "-type", "f"]))

        return o_file

    def index(self, itag, doc, opt):
        
        # opt is a fixed length list, so check for it

        p = []

        if opt[0] == "stop":
            p.append(self.stopfile)

        if opt[1] in self.stemmer_map.keys():
            p.append(self.stemmer_map[opt[1]])
            
        pipeline = ",".join(p)

        i_file  = self.__write_doclist(itag)
        i_file1 = os.path.join(self.env["utils"], "stops")
        o_dir   = os.path.join(self.env["index"], itag)

        # backup existing index
        if os.path.exists(o_dir):
            os.rename(o_dir, os.path.join(self.env["attic"], 
                                          "-".join([itag,str(time.time())])))

        # needed, or else terrier complains
        os.mkdir(o_dir)

        subprocess.check_output([
                os.path.join(self.env["terrier"], "bin/trec_terrier.sh"),
                "-i",
                "-Dcollection.spec="    + i_file,
                "-Dterrier.index.path=" + o_dir,
                "-Dstopwords.filename=" + i_file1,
                "-Dtermpipelines="      + pipeline,
                "-DTrecDocTags.doctag=DOC",
                "-DTrecDocTags.idtag=DOCNO",
                "-DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL",
                "-DTrecDocTags.skip=DOCHDR",
                "-DTrecDocTags.casesensitive=true")


    def retrieve(self, itag, rtag, m, q, q_mode="t"):

        # q is the topic file
        # q_mode is a string like "tdn"

        i_file = q
        o_dir = self.env["runs"]
        o_file_name = rtag

        l = list(q_mode)

        process = []
        skip = []
        for s in ["t", "d", "n"]:
            if s in l:
                process.append(self.query_map[s])
            else:
                skip.append(self.query_map[s])
        process = ",".join(process)
        skip = ",".join(skip)

        i_dir = os.path.join(self.env["index"], itag)
        
        subprocess.check_output([
            os.path.join(self.env["terrier"], "bin/trec_terrier.sh"),
            "-r",
            "-Dterrier.index.path=" + i_dir,
            "-Dtrec.topics=" + i_file,
            "-DTrecQueryTags.doctag=TOP",
            "-DTrecQueryTags.idtag=NUM",
            "-DTrecQueryTags.process=TOP,NUM," + process,
            "-DTrecQueryTags.skip=" + skip,
            "-DTrecQueryTags.casesensitive=false",
            "-Dtrec.model=" + self.model_map[m],
            "-Dtrec.results=" + o_dir,
            "-Dtrec.results.file=" + o_file_name])

    def evaluate(self, rtag, qrels):

        # trec_eval -q QREL_file Retrieval_Results > eval_output

        i_file = os.path.join(self.env["runs"], rtag)
        o_file = os.path.join(self.env["evals"], rtag)

        with open(o_file, "w") as f:
            f.write(subprocess.check_output(
                    [os.path.join(self.env["treceval"], "trec_eval"),
                     "-q",
                     qrels,
                     i_file]))

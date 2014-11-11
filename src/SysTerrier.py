import sys, os, subprocess
import time
from bs4 import BeautifulSoup

class SysTerrier():

    def __init__(self, path):
        self.path = path
        #self.model_map   = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}

        self.model_map = {"bb2": "BB2", "bm25": "BM25", "dfi0": "DFI0", "dfr_bm25": "DFR_BM25", 
                          "dfree": "DFRee", "dirichletlm": "DirichletLM", "dlh": "DLH", 
                          "dlh13": "DLH13", "dph": "DPH", "hiemstra_lm": "Hiemstra_LM", 
                          "ifb2": "IFB2", "in_expb2": "In_expB2", "in_expc2": "In_expC2", 
                          "inb2": "InB2", "inl2": "InL2", "js_kls": "Js_KLs", 
                          "lemurtf_idf": "LemurTF_IDF", "lgd": "LGD", "pl2": "PL2", 
                          "tfidf1": "TFIDF1", "tfidf2": "TFIDF2", "tfidf3": "TFIDF3",
                          "tfidf4": "TFIDF4", "tfidf5": "TFIDF5", "tfidf6": "TFIDF6",
                          "sersimple": "SERSIMPLE", "serbm25": "SERBM25", "dhgb": "DHGB",
                          "xsqra_m": "XSqrA_M"}

        self.stemmer_map = {"p": "PorterStemmer", "w": "WeakPorterStemmer",
                            "s": "EnglishSnowballStemmer"}

    def __write_doclist(self, itag, doc):
        # write Terrier's collection.spec file
        o_file = os.path.join(self.path["index"], ".".join([itag, "terrier"]))
        with open(o_file, "w+b") as f:
            f.write(subprocess.check_output(["find", "-L", doc, "-type", "f"]))
        return o_file

    def __build_termpipeline(self, opt):

        # opt is a fixed length list, so check for it

        p = ["NoOp", "NoOp"]

        stopwords = ""

        if opt[0] != "None":
            p[0] = "Stopwords"
            stopwords = os.path.join(self.path["util"], opt[0])

        if opt[1] in self.stemmer_map.keys():
            p[1] = self.stemmer_map[opt[1]]
            
        return ",".join(p), stopwords

    def __query_file(self, rtag, q):

        # queries are in the dict q
        # Build the query XML, that we want to feed terrier, and write
        # it out to disk.

        soup = BeautifulSoup("<trick></trick>", "xml")

        # float n query tags in the soup

        for num in q.keys():
            T_top = soup.new_tag("top")
            T_num = soup.new_tag("num")
            T_num.string = num
            T_text = soup.new_tag("text")
            T_text.string = q[num]
            T_top.append(T_num)
            T_top.append(T_text)
            soup.trick.append(T_top)
        
        o_file = os.path.join(self.path["run"], ".".join([rtag, "terrier"]))

        # Drop the XML declaration and no more tricks please. Write it
        # out.

        with open(o_file, "w") as f:
            f.write("\n".join(soup.prettify().split("\n")[2:-1]))

        return o_file


    def index(self, itag, doc, opt):

        # print(itag)

        # Terrier needs to be be fed a o_dir, but do nothing if one exists.
        o_dir = os.path.join(self.path["index"], itag)

        if os.path.exists(o_dir):
            print("index(): found, so skipping " + itag)
            return

        os.mkdir(o_dir)

        pipeline, stopwords = self.__build_termpipeline(opt)
        i_file  = self.__write_doclist(itag, doc)
        log     = ""

        try:
           log =  subprocess.check_output(
               [os.path.join(self.path["terrier"], "bin/trec_terrier.sh"),
                "-i",
                "-Dcollection.spec="    + i_file,
                "-Dterrier.index.path=" + o_dir,
                "-Dstopwords.filename=" + stopwords,
                "-Dtermpipelines="      + pipeline,
                "-DTrecDocTags.doctag=DOC",
                "-DTrecDocTags.idtag=DOCNO",
                "-DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL",
                "-DTrecDocTags.skip=DOCHDR",
                "-DTrecDocTags.casesensitive=true"],
               stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            log = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)

        o_log = os.path.join(os.path.join(self.path["index"], itag + ".log"))
        with open(o_log, "w+b") as f:
            f.write(log)

    def retrieve(self, itag, rtag, opt, m, q):

        # print(rtag)

        o_dir  = self.path["run"]
        o_file = rtag
        i_dir  = os.path.join(self.path["index"], itag)
        i_file = self.__query_file(rtag, q)
        log    = ""

        if not os.path.exists(i_dir):
            print("retrieve(): didn't find index " + itag)
            return

        if os.path.exists(os.path.join(o_dir, o_file)):
            print("retrieve(): found, so skipping " + rtag)
            return

        pipeline, stopwords = self.__build_termpipeline(opt)

        # terrier is fed a topic file where all the text resides
        # within the <text> and </text> tags, because picking topic
        # portions by t, d, n is handled at a point in the past by the
        # Topics.query() function. This does away with the need to
        # construct the 'TrecQueryTags.process' and
        # 'TrecQueryTags.skip' parameters here, making things look
        # neater. It so happens, and I know not why, that terrier
        # needs to be told what to 'process' and what to 'skip'
        # simultaniously. 'process' this, this and this, does not
        # imply 'not processing' the others.

        try:
            log = subprocess.check_output(
                [os.path.join(self.path["terrier"], "bin/trec_terrier.sh"),
                 "-r",
                 "-Dterrier.index.path=" + i_dir,
                 "-Dtrec.topics=" + i_file,
                 "-DTrecQueryTags.doctag=TOP",
                 "-DTrecQueryTags.idtag=NUM",
                 "-DTrecQueryTags.process=TOP,NUM,TEXT",
                 "-DTrecQueryTags.skip=",
                 "-DTrecQueryTags.casesensitive=false",
                 "-Dstopwords.filename=" + stopwords,
                 "-Dtermpipelines="      + pipeline,
                 "-Dtrec.model=" + self.model_map[m],
                 "-Dtrec.results=" + o_dir,
                 "-Dtrec.results.file=" + o_file],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            log = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)

        o_log = os.path.join(os.path.join(self.path["run"], rtag + ".log"))
        with open(o_log, "w+b") as f:
            f.write(log)

    def evaluate(self, rtag, qrels):

        # print(rtag)

        o_file = os.path.join(self.path["eval"], rtag)
        i_file = os.path.join(self.path["run"], rtag)

        if not os.path.exists(i_file):
            print("evaluate(): didn't find run " + rtag)
            return

        if os.path.exists(o_file):
            print("evaluate(): found, so skipping " + rtag)
            return
        
        # trec_eval -q QREL_file Retrieval_Results > eval_output
        with open(o_file, "w+b") as f:
            f.write(subprocess.check_output(
                    [os.path.join(self.path["treceval"], "trec_eval"),
                     "-q",
                     qrels,
                     i_file]))

import sys, os, subprocess
import time
import simplejson as json
from bs4 import BeautifulSoup

class SysTerrier():

    def __init__(self, path):
        self.path        = path
        self.model_file  = os.path.join(self.path["TERRIER"], "mods/models.terrier")
        self.model_map   = json.loads(open(self.model_file, "r").read())
        self.stemmer_map = {"po": "PorterStemmer", "wp": "WeakPorterStemmer",
                            "sn": "EnglishSnowballStemmer", "s": "SStemmer"}
        self.qe_map      = {"kl0": "KL",         "kla": "BA",        "kli": "Information",
                            "klm": "KLComplete", "klr": "KLCorrect", "bo1": "Bo1",
                            "bo2": "Bo2"}

    def __write_doclist(self, itag, doc):
        # write Terrier's collection.spec file
        o_file = os.path.join(self.path["INDEX"], itag + ".docs")
        if not os.path.exists(o_file):
            with open(o_file, "w+b") as f:
                f.write(subprocess.check_output(["find", "-L", doc, "-type", "f"]))
        return o_file

    def __build_termpipeline(self, opt):
        p = ["", ""]
        stopp = os.path.join(self.path["MISC"], opt[0])
        p[0]  = "Stopwords"
        if opt[0] == "x":
            p[0]  = "NoOp"
            stopp = ""
        if opt[1] in self.stemmer_map:
            p[1] = self.stemmer_map[opt[1]]
        if opt[1] == "x":
            p[1] = "NoOp"
        return p[0] + "," + p[1], stopp

    def write_file(self, qtag, q):

        # queries are in the dict q
        # Build the query XML, that we want to feed terrier, and write
        # it out to disk.

        soup = BeautifulSoup("<trick></trick>", "xml")

        # float n query tags in the soup

        for num in q:
            T_top = soup.new_tag("TOP")
            T_num = soup.new_tag("NUM")
            T_num.string = str(num)
            T_text = soup.new_tag("TEXT")
            T_text.string = q[num]
            T_top.append(T_num)
            T_top.append(T_text)
            soup.trick.append(T_top)
        
        # Drop the XML declaration, remove <trick>, write it out.

        o_file = os.path.join(self.path["RUNS"], qtag + ".queries")
        if not os.path.exists(o_file):
            with open(o_file, "w") as f:
                f.write("\n".join(soup.prettify().split("\n")[2:-1]))

        return o_file


    def index(self, itag, doc, opt):

        # print(itag)

        # Terrier needs to be be fed a o_dir, but do nothing if one exists.
        o_dir = os.path.join(self.path["INDEX"], itag)

        if os.path.exists(o_dir):
            print("index(): found, so skipping " + itag)
            return

        os.mkdir(o_dir)

        pipeline, stopwords = self.__build_termpipeline(opt)
        i_file  = self.__write_doclist(itag, doc)
        log     = ""

        # Recommended at http://ir.dcs.gla.ac.uk/wiki/Terrier/Disks1&2
        # -DTrecDocTags.process=TEXT,TITLE,HEAD,HL
        # Recommended at http://ir.dcs.gla.ac.uk/wiki/Terrier/Disks4&5
        # -DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL
        # To be able to process all documents in CDs 1 - 5 use everything and skip nothing:
        # "-DTrecDocTags.process=" 
        # "-DTrecDocTags.skip="

        try:
           log =  subprocess.check_output(
               [os.path.join(self.path["TERRIER"], "bin/trec_terrier.sh"),
                "-i",
                "-Dcollection.spec="    + i_file,
                "-Dterrier.index.path=" + o_dir,
                "-Dstopwords.filename=" + stopwords,
                "-Dtermpipelines="      + pipeline,
                "-DTrecDocTags.doctag=DOC",
                "-DTrecDocTags.idtag=DOCNO",
                "-DTrecDocTags.process=",
                "-DTrecDocTags.skip=",
                "-DTrecDocTags.casesensitive=false"],
               stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            log = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)

        o_log = os.path.join(os.path.join(self.path["INDEX"], itag + ".log"))
        with open(o_log, "w+b") as f:
            f.write(log)

    def retrieve(self, itag, rtag, opt, m, q, qe):

        # print(rtag)

        o_dir     = self.path["RUNS"]
        o_file    = rtag
        i_dir     = os.path.join(self.path["INDEX"], itag)
        i_file    = q

        tfnorm    = ""
        if m[1]:
            tfnorm = "-c " + m[1]

        qe_ctrl   = ""
        qe_ordr   = ""
        qe_model  = ""
        qe_terms  = "0"
        qe_docs   = "0"
        qe_switch = ""

        if qe[0] != "x":
            qe_ctrl   = "qe:QueryExpansion"
            qe_ordr   = "QueryExpansion"
            qe_model  = "org.terrier.matching.models.queryexpansion." + self.qe_map[qe[0]]
            qe_terms  = qe[1]
            qe_docs   = qe[2]
            qe_switch = "-q"

        log = ""

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
        # Query.query() function. This does away with the need to
        # construct the 'TrecQueryTags.process' and
        # 'TrecQueryTags.skip' parameters here, making things look
        # neater. It so happens, and I know not why, that terrier
        # needs to be told what to 'process' and what to 'skip'
        # simultaniously. 'process' this, this and this, does not
        # imply 'not processing' the others.
        #
        # trecbox's way of processing TREC queries (across all 5 disks):
        # "-DTrecQueryTags.doctag=TOP",
        # "-DTrecQueryTags.idtag=NUM",
        # "-DTrecQueryTags.process=TOP,NUM,TEXT",
        # "-DTrecQueryTags.skip=",
        # "-DTrecQueryTags.casesensitive=false",
        #
        # terrier's way of processing TREC queries for Disks 4 & 5:
        # "-DTrecQueryTags.doctag=TOP",
        # "-DTrecQueryTags.idtag=NUM",
        # "-DTrecQueryTags.process=TOP,NUM,TITLE",
        # "-DTrecQueryTags.skip=DESC,NARR",
        # "-DTrecQueryTags.casesensitive=false",

        try:
            log = subprocess.check_output(
                [os.path.join(self.path["TERRIER"], "bin/trec_terrier.sh"),
                 "-r",
                 qe_switch,
                 tfnorm,
                 "-Dterrier.index.path=" + i_dir,
                 "-Dtrec.topics=" + i_file,
                 "-DTrecQueryTags.doctag=TOP",
                 "-DTrecQueryTags.idtag=NUM",
                 "-DTrecQueryTags.process=TOP,NUM,TEXT",
                 "-DTrecQueryTags.skip=",
                 "-DTrecQueryTags.casesensitive=false",
                 "-Dstopwords.filename=" + stopwords,
                 "-Dtermpipelines=" + pipeline,
                 "-Dtrec.model=" + self.model_map[m[0]],
                 "-Dquerying.postprocesses.controls=" + qe_ctrl,
                 "-Dquerying.postprocesses.order=" + qe_ordr,
                 "-Dtrec.qe.model=" + qe_model,
                 "-Dexpansion.terms=" + qe_terms,
                 "-Dexpansion.documents=" + qe_docs,
                 "-Dtrec.results=" + o_dir,
                 "-Dtrec.results.file=" + o_file],
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            log = str(e.cmd) + "\n" + str(e.returncode) + "\n" + str(e.output)

        o_log = os.path.join(os.path.join(self.path["RUNS"], rtag + ".log"))
        with open(o_log, "w+b") as f:
            f.write(log)

    def evaluate(self, rtag, qrels):

        # print(rtag)

        o_file  = os.path.join(self.path["EVALS"], rtag)
        i_file  = os.path.join(self.path["RUNS"], rtag)

        if not os.path.exists(i_file):
            print("evaluate(): didn't find run " + rtag)
            return

        if os.path.exists(o_file):
            print("evaluate(): found, so skipping " + rtag)
            return
        
        # trec_eval -q qrels run > eval_output
        with open(o_file, "w+b") as f:
            f.write(subprocess.check_output(
                    [os.path.join(self.path["TRECEVAL"], "trec_eval"),
                     "-q",
                     qrels,
                     i_file]))

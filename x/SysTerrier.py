import sys, os, subprocess
import time
from bs4 import BeautifulSoup

class SysTerrier():

    def __init__(self, env):
        self.env = env
        self.query_map   = {"t": "TITLE", "d": "DESC", "n": "NARR"}
        self.model_map   = {"bm25": "BM25", "dfr": "DFI0", "tfidf": "TF_IDF"}
        self.stemmer_map = {"porter": "PorterStemmer", "weak-porter": "WeakPorterStemmer", 
                            "snowball": "EnglishSnowballStemmer"}

    def __write_doclist(self, itag, doc):
        # write Terrier's collection.spec file
        o_file = os.path.join(self.env["index"], ".".join([itag, "terrier"]))
        with open(o_file, "w") as f:
            f.write(subprocess.check_output(["find", doc, "-type", "f"]))
        return o_file

    def __build_termpipeline(self, opt):

        # opt is a fixed length list, so check for it

        p = ["NoOp", "NoOp"]
        stopwords = ""

        if opt[0] != "None":
            p[0] = "Stopwords"
            stopwords = os.path.join(self.env["utils"], opt[0])

        if opt[1] in self.stemmer_map.keys():
            p[1] = self.stemmer_map[opt[1]]
            
        return ",".join(p), stopwords

    def __query_file(self, rtag, q):

        # queries are in a dict q
        # build the query XML, that we want to feed terrier, and write
        # it out to disk

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
        
        o_file = os.path.join(self.env["runs"], ".".join([rtag, "terrier"]))

        # Drop the XML declaration and no more tricks please. Write it
        # out.

        with open(o_file, "w") as f:
            f.write("\n".join(soup.prettify().split("\n")[2:-1]))

        return o_file


    def index(self, itag, doc, opt):
        
        pipeline, stopwords = self.__build_termpipeline(opt)
        i_file  = self.__write_doclist(itag, doc)
        o_dir   = os.path.join(self.env["index"], itag)

        # backup existing index to an attic by time stamping it

        if os.path.exists(o_dir):
            os.rename(o_dir, os.path.join(self.env["attic"], 
                                          "-".join([itag,str(time.time())])))

        # needed, or else Terrier complains

        os.mkdir(o_dir)

        subprocess.check_output([
                os.path.join(self.env["terrier"], "bin/trec_terrier.sh"),
                "-i",
                "-Dcollection.spec="    + i_file,
                "-Dterrier.index.path=" + o_dir,
                "-Dstopwords.filename=" + stopwords,
                "-Dtermpipelines="      + pipeline,
                "-DTrecDocTags.doctag=DOC",
                "-DTrecDocTags.idtag=DOCNO",
                "-DTrecDocTags.process=TEXT,H3,DOCTITLE,HEADLINE,TTL",
                "-DTrecDocTags.skip=DOCHDR",
                "-DTrecDocTags.casesensitive=true"])


    def retrieve(self, itag, rtag, opt, m, q):

        pipeline, stopwords = self.__build_termpipeline(opt)
        i_dir = os.path.join(self.env["index"], itag)
        i_file = self.__query_file(rtag, q)
        o_dir = self.env["runs"]
        o_file = rtag

        # terrier is fed a topic file where all the text resides
        # within the <text> and </text> tags, because picking topic
        # portions by t, d, n is handled at a point in the past by the
        # Topics.query() function. This does away with the need to
        # construct the 'TrecQueryTags.process' and
        # 'TrecQueryTags.skip' parameters here, making things look
        # neater. It so happens, and I know not why, that terrier
        # needs to be told what to 'process' and what to 'skip'
        # simultaniously. 'process' this, this and this, does not
        # imply not doing anything about them.

        subprocess.check_output([
            os.path.join(self.env["terrier"], "bin/trec_terrier.sh"),
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
            "-Dtrec.results.file=" + o_file])

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

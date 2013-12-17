import sys
from Sys import *
from bs4 import BeautifulSoup

#indri-5.0/buildindex/IndriBuildIndex parameter_file
#-corpus.path=/path/to/file_or_directory
#-corpus.class=trectext
#-index=/path/to/repository
#-memory 100M
#-stopper.word=stopword
#-stemmer.name=stemmername
#-field.name=fieldname

#field : a complex element specifying the fields to index as data, eg
#TITLE. This parameter can appear multiple times in a parameter
#file. If provided on the command line, only the first field specified
#will be indexed.

#indri-5.0/runquery/IndriRunQuery query_parameter_file -count=1000 -index=/path/to/index -trecFormat=true > result_file
#-query="apple juice" or -query="#combine(apple juice)"

#TREC queries cannot be fed into Indri directly, punctuations need to
#be removed. One simple strategy is to replace everything that's not a
#number (0x30-0x39) or letter with a space (0x20). However,
#tokenization should be performed similar to how the indexer indexes
#texts. And in Indri, "U.S." will be translated into "us" in the
#indexer.

class SysIndri(Sys):

    def __init__(self, env, doc, topic, model, qrel):
        Sys.__init__(self, env, doc, topic, model, qrel)
        self.sys_id = "I"
        self.index_id = ".".join([self.sys_id, self.doc.name])
        self.run_id = ".".join([self.sys_id, self.doc.name, 
                                self.model.name, self.topic.mode])
        self.iparam_f = ".".join(["param", "i", self.index_id])
        self.qparam_f = ".".join(["param", "q", self.run_id])
        self.param = {
            "iparam": os.path.join(self.env["index"], self.iparam_f),
            "index": os.path.join(self.env["index"], self.index_id),
            "topics": os.path.join(self.env["topics"], self.topic.file),
            "qparam": os.path.join(self.env["runs"], self.qparam_f),
            "runs": os.path.join(self.env["runs"], self.run_id),
            "evals": os.path.join(self.env["evals"], self.run_id)
            }

    def shapeup_xml(self, l):

        l_ = []
        n = 0

        for i in range(len(l)):
            l[i] = l[i].lstrip().rstrip()
            l[i] = l[i].lstrip("\n").rstrip("\n")
            l_.append(l[i])
            n = len(l_) - 1

            if i == 0:
                continue

            if l_[n].startswith("</"):
                if not l_[n-1].startswith("<"):
                    e  = l_.pop()
                    e1 = l_.pop()
                    e2 = l_.pop()
                    l_.append(e2 + e1 + e)
                    n = len(l_) - 1
                
        return "\n".join(l_)
        
    def index(self):

        # consider backing up an existing one with a stamp instead of
        # deleting it
        #if os.path.exists(self.param["index"]):
        #    os.removedirs(self.param["index"])
        #os.mkdir(self.param["index"])

        # build and write Indri's index param file

        soup = BeautifulSoup("<parameters></parameters>", "xml")

        T_corpus = soup.new_tag("corpus")
        soup.parameters.append(T_corpus)

        T_path = soup.new_tag("path")
        T_path.string = self.doc.path
        soup.parameters.corpus.append(T_path)

        T_class = soup.new_tag("class")
        T_class.string = "trectext"
        soup.parameters.corpus.append(T_class)

        T_index = soup.new_tag("index")
        T_index.string = self.param["index"]
        soup.parameters.append(T_index)

        # Attach the 5 <field> tags

        for i in range(5):
            T_field = soup.new_tag("field")
            soup.parameters.append(T_field)

        # iterate over 5 <field> tags adding the <name> child to each

        TREC_field = ["TEXT", "H3", "DOCTITLE", "HEADLINE", "TTL"]
        i = 0

        T_field = soup.parameters.field
        while(T_field):
            T_name = soup.new_tag("name")
            T_name.string = TREC_field[i]
            i += 1
            T_field.append(T_name)
            T_field = T_field.find_next_sibling("field")

        # get rid of the first line of the xml introduced by BeautifulSoup
        # and shape it up for Indri to consume

        with open(self.param["iparam"], "w") as f:
            f.write(self.shapeup_xml(soup.prettify().split("\n")[1:]))
            
        args = {
            "exec": "/home/rup/indri-5.5/buildindex/IndriBuildIndex",
            "param_file": self.param["iparam"]
            }

        subprocess.check_output([args["exec"], args["param_file"]])

    def retrieve(self, q):
        
        # determine query
        # q is a dict here
        
        # build the query-param xml and write it out to disk
        dumb = ""

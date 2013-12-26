from bs4 import BeautifulSoup
import string

class Topics():
    def __init__(self, f, mode = "t"):
        self.file = f
        self.mode = mode.lower()

    def query_L(self):
        return "/home/rup/lucene.TREC/test-data/title-queries.301-450"

    def query_T(self):
        return self.mode
        
    def query_I(self):

        #if ever you want to prettyprint the soup without the tricks
        #print "\n".join(soup.prettify().split("\n")[2:-1])

        soup = self.__hack_n_hew()

        q = {}

        # wade in the soup and
        # return a dict of query text indexed by qid

        for top in soup.find_all("top"):
            n = top.num.string.lstrip().rstrip()
            q[n] = ""
            for m in list(self.mode):
                if m == "t":
                    q[n] += " " + top.title.string
                if m == "d":
                    q[n] += " " + top.desc.string
                if m == "n":
                    q[n] += " " + top.narr.string

        return q


    def __hack_n_hew(self):

        # sanitize old TREC topics for Indri's consumption
        # add closing tags, purge punctuation and return a bowl of soup

        with open(self.file, "r") as f_:
            txt = f_.read()
            
        in_tag = False
        s = ""
        c_ = ""

        for c in txt:
            if c == "\n" or c == "\r" or c == "\t":
                continue
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
                s += c
                if s == "<title>":
                    s = "</num>" + s
                if s == "<desc>":
                    s = "</title>" + s
                if s == "<narr>":
                    s = "</desc>" + s
                if s == "</top>":
                    s = "</narr>" + s
                c_ += s
                s = ""
                continue

            if(in_tag):
                s += c
            else:
                c_ += c
    
        soup = BeautifulSoup("<trick>" + c_ + "</trick>", "xml")

        for num in soup.find_all("num"):
            num.string = num.string.replace("Number:", "")
        for desc in soup.find_all("desc"):
            desc.string = desc.string.replace("Description:", "")
        for narr in soup.find_all("narr"):
            narr.string = narr.string.replace("Narrative:", "")

        # purge all punctuation from the text
        for i in soup.find_all(True):
            if i.string:
                i.string = str(i.string).translate(None, string.punctuation)

        return soup

from bs4 import BeautifulSoup
import string, re, sys

class Topics():

    def __init__(self, f):
        self.file = f

    def query(self, opt, mode="t", qlist=[]):

        # Usually, query() should return a malleable form of the query
        # text, read in from a file on disk. For indri, lucene and
        # terrier it returns a dict. It's recommended you don't return
        # paths to a file on disk. If you have made a decision to dump
        # the stuff in memory to disk at this point and return a path
        # to the file, it looks bad. Let the systems do whatever they
        # want with it.

        q = {}
        opt = opt.lower()
        mode = mode.lower()
        qlist = set(qlist)
        soup = self.__hack_n_hew()

        # If ever you want to prettyprint the soup without the tricks
        # print "\n".join(soup.prettify().split("\n")[2:-1])

        # indri and lucene can't stand puncs
        if opt == "indri" or opt == "lucene":
            soup = self.__wipe_punctuations(soup)

        # Wade in the soup and return a dict of query text picked by
        # 'mode', scoped by 'qlist' (if given) and indexed by qid

        for top in soup.find_all("top"):
            n = top.num.string.lstrip().rstrip()
            if qlist and (n not in qlist):
                continue
            q[n] = ""
            for m in list(mode):
                if m == "t":
                    q[n] += " " + top.title.string
                if m == "d":
                    q[n] += " " + top.desc.string
                if m == "n":
                    q[n] += " " + top.narr.string
            q[n] = q[n].lstrip().rstrip()

        return q

    def __name(self, tag):
        return tag.lstrip("<").rstrip(">").lstrip("/")

    def __is_closing(self, tag):
        if tag[1] == "/":
            return True
        else:
            return False

    def __is_opening(self, tag):
        if tag[1] != "/":
            return True
        else:
            return False

    def __opening_of(self, tag):
        return "<" + self.__name(tag) + ">"
    
    def __closing_of(self, tag):
        return "</" + self.__name(tag) + ">"

    def __wipe_punctuations(self, soup):
        for i in soup.find_all(True):
            if i.string:
                i.string = str(i.string).translate(None, string.punctuation)
        return soup

    def __hack_n_hew(self):

        # sanitize old TREC topics for a system's consumption: add
        # closing tags and return a bowl of soup

        with open(self.file, "r") as f_:
            txt = f_.read()
            
        in_tag = False
        s = ""
        c_ = ""

        stack = []
        stack1 = []
        
        for c in txt:
            if c == "\n" or c == "\r" or c == "\t":
                continue
            if c == "<":
                stack1.append(c)
                in_tag = True
            elif c == ">":
                if not stack1:
                    continue
                else:
                    stack1.pop()
                s += c
                in_tag = False

                # This block of code makes __hack_n_hew()
                # idempotent. Which means, old TREC SGML topic files
                # that have no closing tags, as well as well formed
                # TREC XML topic files will pass through smoothly,
                # ready for consumption by an XML parser.

                # algorithm:
                # Keeps pushing the opening tags to a stack. If an
                # incoming opening tag is not the TREC tag "<top>",
                # and the top of the stack is some other opening tag,
                # the incoming tag is sent to the output stream with
                # the closing of the stack top as a prefix and the
                # stack is popped. If the incoming tag is a closing
                # tag and the stack top is its corresponing opening,
                # then simply the stack is popped. Again, if the
                # incoming tag is a closing tag and the stack top
                # holds an opening tag, then the incoming tag is sent
                # to the stream prefixed with the closing of the stack
                # top, and the stack is popped. At any moment the
                # stack contains only opening tags, or is empty if the
                # closing TREC tag "</top>" has been read.

                if s == "<top>":
                    stack.append(s)
                elif self.__is_opening(s):
                    top = stack.pop()
                    if top == "<top>" or top == "<fac>":
                        stack.append(top)
                        stack.append(s)
                    else:
                        stack.append(s)
                        s = self.__closing_of(top) + s
                elif self.__is_closing(s):
                    top = stack.pop()
                    if top != self.__opening_of(s):
                        s = self.__closing_of(top) + s
                        stack.pop()

                # print stack
                print s

                c_ += s
                s = ""
                continue

            if(in_tag):
                s += c
            else:
                c_ += c
    
        soup = BeautifulSoup("<trick>" + c_ + "</trick>", "xml")

        for num in soup.find_all("num"):
            num.string = num.string.lstrip().rstrip()
            num.string = re.sub(r'^Number:[ ]*', "", num.string)
        for desc in soup.find_all("desc"):
            desc.string = desc.string.lstrip().rstrip()
            desc.string = re.sub(r'^Description:[ ]*', "", desc.string)
        for narr in soup.find_all("narr"):
            narr.string = narr.string.lstrip().rstrip()
            narr.string = re.sub(r'^Narrative:', "", narr.string)

        return soup

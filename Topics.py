from collections import OrderedDict as OD
from bs4 import BeautifulSoup
import re, sys

class Topics():

    def __init__(self, f):
        self.file = f

    def query(self, opt=None, qtdn="T", qlist=None):

        # Usually, query() should return a malleable form of the query
        # text, read in from a file on disk. For indri, lucene and
        # terrier it returns a dict. It's recommended you don't return
        # paths to a file on disk. Let the systems do whatever they
        # want with it.

        q    = OD()
        if opt:
            opt = opt.lower()

        soup = self.__hack_n_hew()

        # To prettyprint the soup without the tricks
        # print "\n".join(soup.prettify().split("\n")[2:-1])

        # indri and lucene can't stand puncs
        if opt == "indri" or opt == "lucene":
            soup = self.__wipe_punctuations(soup)

        # Wade in the soup and return a dict of query text picked by
        # 'qtdn', scoped by 'qlist' (if given) and indexed by qid

        for top in soup.find_all("top"):
            # lower (older) qids are padded with zeros, as in '002'
            # int() drops these leading zeros
            n = int(top.num.string.lstrip().rstrip())
            if  qlist and (n not in qlist):
                continue
            q[n] = ""
            for m in list(qtdn):
                if m == "T":
                    if top.title != None:
                        q[n] += " " + top.title.string
                if m == "D":
                    if top.desc != None:
                        q[n] += " " + top.desc.string
                if m == "N":
                    if top.narr != None:
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
                # the regex is identical to the value of Python's
                # string.punctiation constant
                i.string = re.sub("[!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]", " ", i.string)
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
                c = " "
            elif c == "<":
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
                # idempotent. Old TREC SGML topic files (that have no
                # closing tags) will be corrected , and well formed
                # TREC XML topic files will pass through unchanged,
                # ready for consumption by an XML parser.
                #
                # algorithm:
                #
                # Push the first (opening) tag to a stack and then
                # branch depending on what type of tag arrives next
                # from the input stream and what tag is at the top of
                # the stack. Only opening tags are pushed. So at any
                # instant the stack contains opening tags, or is empty
                # if </top> has been read. Here are the situations to
                # handle, depending on the incoming tag:
                #
                # a) opening tag
                # If it is <top> then push. If not then check the
                # top. If the top is also some other opening tag, the
                # incoming tag is sent to the output stream with the
                # closing of the top as a prefix and then pop.
                #
                # b) closing tag
                # i) If the top is its corresponing opening, then pop.
                # ii) If the top holds an opening tag, then the
                # incoming tag is sent to the stream prefixed with the
                # closing of the top, and then pop.
                #
                # NOTE: BAD HACK! The old TREC topic files (1-150)
                # have a <fac></fac> nesting inside <top></top>. I
                # close <fac> immediately with a </fac>, close all
                # tags inside <fac> as usual, and throw away
                # </fac>. This potentially breaks the original
                # structure, leading to a useless <fac></fac> item but
                # solves my problem for the time being because I never
                # make use of the contents of <fac>.

                if s == "<top>":
                    stack.append(s)
                elif s == "</fac>":
                    s = ""
                    continue
                elif self.__is_opening(s):
                    top = stack.pop()
                    if top == "<top>":
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

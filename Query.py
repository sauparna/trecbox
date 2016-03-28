from collections import OrderedDict as OD
from bs4 import BeautifulSoup
import re, sys, os

class Query():

    def __init__(self, iqf, part="T", qids=None, kind=None):
        self.iqf = iqf
        self.oqf = ""
        self.q  = OD()
        self.n  = 0
        self.part = part
        self.qids = qids
        self.kind = kind
        if kind:
            self.kind = self.kind.lower()

    def parse(self):

        # Usually, query() should return a malleable form of the query
        # text, read in from a file on disk. For indri, lucene and
        # terrier it returns a dict.

        soup = self.__hack_n_hew()

        # To prettyprint the soup without the tricks
        # print("\n".join(soup.prettify().split("\n")[2:-1]))

        # indri and lucene can't stand puncs
        if self.kind == "indri" or self.kind == "lucene":
            soup = self.__wipe_punctuations(soup)

        # Wade in the soup and return a dict of query text picked by
        # 'self.part', scoped by 'self.qids' (if given) and indexed by qid

        for top in soup.find_all("top"):
            
            # lower (older) qids are prefixed with zeros, as in '002'
            # so typecasting to int() drops these leading zeros

            qid = int(top.num.string.lstrip().rstrip())

            if  self.qids and (qid not in self.qids):
                continue
            self.q[qid] = ""
            for m in list(self.part):
                if m == "T":
                    if top.title != None:
                        self.q[qid] += " " + top.title.string
                if m == "D":
                    if top.desc != None:
                        self.q[qid] += " " + top.desc.string
                if m == "N":
                    if top.narr != None:
                        self.q[qid] += " " + top.narr.string
            self.q[qid] = self.q[qid].lstrip().rstrip()
            self.n = self.n + 1
        
        return self.q

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

        with open(self.iqf, "r") as f_:
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
        for title in soup.find_all("title"):
            title.string = title.string.lstrip().rstrip()
            title.string = re.sub(r'^Topic:[ ]*', "", title.string)
        for desc in soup.find_all("desc"):
            desc.string = desc.string.lstrip().rstrip()
            desc.string = re.sub(r'^Description:[ ]*', "", desc.string)
        for narr in soup.find_all("narr"):
            narr.string = narr.string.lstrip().rstrip()
            narr.string = re.sub(r'^Narrative:', "", narr.string)

        return soup

    def write_xml(self, o_dir, oqf):
        
        # Build the query XML, that we want to feed terrier, and write
        # it out to disk.

        soup = BeautifulSoup("<trick></trick>", "xml")

        # float n query tags in the soup

        for num in self.q:
            T_top = soup.new_tag("TOP")
            T_num = soup.new_tag("NUM")
            T_num.string = str(num)
            T_text = soup.new_tag("TEXT")
            T_text.string = self.q[num]
            T_top.append(T_num)
            T_top.append(T_text)
            soup.trick.append(T_top)
            
        # Drop the XML declaration, remove <trick>, write it out.

        o_file = os.path.join(o_dir, oqf)
        with open(o_file, "w") as f:
            f.write("\n".join(soup.prettify().split("\n")[2:-1]))

        self.oqf = o_file
        return self.oqf

    def write_plaintext(self, o_dir, oqf):
        
        # a query per line

        o_file = os.path.join(o_dir, oqf)
        with open(o_file, "w") as f:
            for num in self.q:
                f.write(self.q[num] + "\n")

        self.oqf = o_file
        return self.oqf

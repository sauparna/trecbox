from bs4 import BeautifulSoup
import string

class Topics():

    def __init__(self, f, mode="t"):

        self.file = f
        self.mode = mode.lower()

    def query(self, opt):

        opt = opt.lower()

        if opt == "indri" or opt == "lucene":

            #return "/home/palchowdhury/ir/topics/title-queries.301-450"

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
            
        elif opt == "terrier":

            return self.file


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
        return "<" + name(tag) + ">"
    
    def __closing_of(self, tag):
        return "</" + name(tag) + ">"

    def __hack_n_hew(self):

        # sanitize old TREC topics for Indri's consumption
        # add closing tags, purge punctuation and return a bowl of soup

        with open(self.file, "r") as f_:
            txt = f_.read()
            
        in_tag = False
        s = ""
        c_ = ""

        stack = []

        for c in txt:
            if c == "\n" or c == "\r" or c == "\t":
                continue
            if c == "<":
                in_tag = True
            elif c == ">":
                s += c
                in_tag = False

                # This block of code makes __hack_n_hew()
                # idempotent. Which means, old TREC SGML topic files
                # that have no closing tags, as well as well formed
                # TREC XML topic files will pass through smoothly,
                # ready for consumption by an XML parser.

                # Keeps pushing the opening tags to a stack. If an
                # incoming opening tag is not the topmost tag (<top>),
                # and the top of the stack is another opening tag, the
                # incoming tag is sent to the output stream with the
                # closing of the top as a prefix and the stack is
                # popped. If the incoming tag is a closing tag and the
                # stack top is its corresponing opening, then simply
                # the stack is popped. Again, if the incoming tag is a
                # closing tag and the stack top holds an opening tag,
                # then the incoming tag is sent to the stream prefixed
                # with the closing of the top, and the stack is
                # popped. At any moment the stack contains only
                # opening tags, or is empty if the closing topmost tag
                # has been read.

                if s == "<top>":
                    stack.append(s)
                elif is_opening(s):
                    top = stack.pop()
                    if top == "<top>":
                        stack.append(top)
                        stack.append(s)
                    else:
                        stack.append(s)
                        s = closing_of(top) + s
                elif is_closing(s):
                    top = stack.pop()
                    if top != opening_of(s):
                        s = closing_of(top) + s
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

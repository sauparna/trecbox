from bs4 import BeautifulSoup
import sys, subprocess, re

def __name(tag):
    return tag.lstrip("<").rstrip(">").lstrip("/")

def __is_closing(tag):
    if tag[1] == "/":
        return True
    else:
        return False

def __is_opening(tag):
    if tag[1] != "/":
        return True
    else:
        return False

def __opening_of(tag):
    return "<" + __name(tag) + ">"
    
def __closing_of(tag):
    return "</" + __name(tag) + ">"

def __wipe_punctuations(soup):
    for i in soup.find_all(True):
        if i.string:
            i.string = str(i.string).translate(None, string.punctuation)
    return soup

def hack_n_hew(f):

    # sanitize old TREC topics for a system's consumption: add
    # closing tags and return a bowl of soup

    with open(f, "r") as f_:
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
                elif __is_opening(s):
                    top = stack.pop()
                    if top == "<top>":
                        stack.append(top)
                        stack.append(s)
                    else:
                        stack.append(s)
                        s = __closing_of(top) + s
                elif __is_closing(s):
                    top = stack.pop()
                    if top != __opening_of(s):
                        s = __closing_of(top) + s
                        stack.pop()

                # print stack
                # print s

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


def main(argv):
    soup = hack_n_hew(argv[1])
    print "\n".join(soup.prettify().split("\n")[2:-1])

if __name__ == "__main__":
    main(sys.argv)

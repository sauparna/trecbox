import sys, os
import simplejson as json
from SysTerrier import *

from Topics import Topics

# TODO: Topics.query() returns t, d, n as one block of text. Make it
# return the parts separately so that they can be tagged in the XML.

def init(f):
    path = json.loads(open(f, "r").read())
    path["o_base"] = os.path.join(path["base"], path["o_base"])
    for k in path["in"].keys():
        path["in"][k] = os.path.join(path["base"], path["in"][k])
    for k in path["out"].keys():
        path["out"][k] = os.path.join(path["o_base"], path["out"][k])
    # # DEBUG
    # print json.dumps(path, sort_keys=True, indent=4 * ' ')

    # flatten the path dict before passing it on to systems
    path.update(dict(path["in"].items() + path["out"].items()))
    del(path["in"])
    del(path["out"])
    # # DEBUG
    # print json.dumps(path, sort_keys=True, indent=4 * ' ')
    return path

def main(argv):
    if len(argv) != 3:
        print "USAGE: python weedtopics.py <conf> <TREC topic file>"
        sys.exit(0)

    conf_f = argv[1]
    topic_f = argv[2]
    path = init(conf_f)
    t = Topics(topic_f)
    q = t.query("terrier", "tdn")
    print q
    sys.exit(0)
    # float n query tags in the soup
    soup = BeautifulSoup("<trick></trick>", "xml")
    for num in q.keys():
        T_top = soup.new_tag("top")
        T_num = soup.new_tag("num")
        T_num.string = num
        T_text = soup.new_tag("text")
        T_text.string = q[num]
        T_top.append(T_num)
        T_top.append(T_text)
        soup.trick.append(T_top)
        
    o_file = os.path.join(path["topic"], "weeded", os.path.basename(topic_f))

    # Drop the XML declaration and no more tricks please. Write it
    # out.
    with open(o_file, "w") as f:
        f.write("\n".join(soup.prettify().split("\n")[2:-1]))
        
if __name__ == "__main__":
   main(sys.argv)

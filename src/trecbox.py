import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def spin(s, c, n):
    sys.stdout.write("\r" + s + " " + str(c) + "/" + str(n))
    sys.stdout.flush()

def backup(path, name):
    # time-stamp and stow away an existing experiment directory
    old = path["o_base"]
    new = os.path.join(path["attic"], name + "-" + str(time.time()))
    os.rename(old, new)
    return "Backed up " + old + " to "  + new

def create_dir(path):
    os.mkdir(path["o_base"])
    os.mkdir(path["run"])
    os.mkdir(path["eval"])
    return "Created " + path["o_base"]

def init(f, f1, name):
    path = json.loads(open(f1, "r").read())
    path["o_base"] = os.path.join(path["base"], path["o_base"], name)
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

    layout = json.loads(open(f, "r").read())
    s = None
    if layout["system"] == "terrier":
        s = SysTerrier(path)
    elif layout["system"] == "indri":
        s = SysIndri(path)
    elif layout["system"] == "lucene":
        s = SysLucene(path)
    else:
        print "Unknown system. Exiting."
        sys.exit(0)

    return layout, path, s

def index(layout, path, s):
    matrix = layout["matrix"]
    models = layout["models"]
    stems  = layout["stems"]
    c = 1
    doc = []
    for i in matrix.keys():
        doc.append(matrix[i][0])
    doc = list(set(doc))
    n = len(doc) * len(stems)
    for d in doc:
        d_path = os.path.join(path["doc"], d)
        for j in stems:
            spin("INDEX:", c, n); c+=1
            itag = d+"."+j
            if os.path.exists(os.path.join(path["index"], itag)):
                print "\rINDEX: " + itag + " exists, skipped."
                continue
            s.index(itag, d_path, ["stop", j])
    print

def retrieve(layout, path, s):
    matrix = layout["matrix"]
    models = layout["models"]
    stems  = layout["stems"]
    system = layout["system"]
    c = 1
    n = len(matrix.keys()) * len(stems) * len(models)
    for i in matrix.keys():
        d  = matrix[i][0]
        t_ = matrix[i][1].split(":")
        t_parts = len(t_)
        if t_parts < 2:
            print "ERROR: Layout doesn't specify topic information correctly."
            sys.exit(0)
        t_path = os.path.join(path["topic"], t_[0])
        t_mode = t_[1]
        t = Topics(t_path)
        if t_parts == 3:
            t_qid = os.path.join(path["topic"], t_[1])
            q = t.query(system, t_mode, t_qid)
        else:
            q = t.query(system, t_mode)
        for j in stems:
            for k in models:
                spin("RETRIEVE:", c, n); c+=1
                s.retrieve(d+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    print

def evaluate(layout, path, s):
    matrix = layout["matrix"]
    models = layout["models"]
    stems  = layout["stems"]
    c = 1
    n = len(matrix.keys()) * len(stems) * len(models)
    for i in matrix.keys():
        qrel_path = os.path.join(path["qrel"], matrix[i][2])
        for j in stems:
            for k in models:
                spin("EVALUATE:", c, n); c+=1
                s.evaluate(i+"."+j+"."+k, qrel_path)
    print

def main(argv):

    if len(argv) != 3:
        print "USAGE: python trecbox.py <layout file> <conf file>"
        sys.exit(0)
    exp   = argv[1]
    name  = os.path.basename(argv[1])
    conf  = argv[2]
    layout, path, s = init(exp, conf, name);
    opt = int(raw_input("0. all\n1. index\n2. retreive\n3. evaluate\n4. quit\n?"))

    if opt not in [0,1,2,3,4]:
        print "ERROR: Unknown option."
        sys.exit(0)

    if opt == 4:
        print "EXIT"
        sys.exit(0)

    if os.path.exists(path["o_base"]):
        print "INFO: Experiment '" + name + "'"
        if opt == 0:
            print "INFO: " + backup(path, name)
            print "INFO: " + create_dir(path)
            index(layout, path, s)
            retrieve(layout, path, s)
            evaluate(layout, path, s)
        if opt == 1:
            print "INFO: " + backup(path, name)
            print "INFO: " + create_dir(path)
            index(layout, path, s)
        elif opt == 2:
            retrieve(layout, path, s)
        elif opt == 3:
            evaluate(layout, path, s)
    else:
        print "INFO: " + create_dir(path)
        if opt == 0:
            index(layout, path, s)
            retrieve(layout, path, s)
            evaluate(layout, path, s)
        if opt == 1:
            index(layout, path, s)
        elif opt == 2:
            print "INFO: index + retrieve"
            index(layout, path, s)
            retrieve(layout, path, s)
        elif opt == 3:
            print "INFO: index + retrieve + evaluate"
            index(layout, path, s)
            retrieve(layout, path, s)
            evaluate(layout, path, s)

if __name__ == "__main__":
   main(sys.argv)

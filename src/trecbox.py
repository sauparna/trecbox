import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def spin(s, c, n):
    sys.stdout.write("\r" + s + " " + str(c) + "/" + str(n))
    sys.stdout.flush()

def init(f, f1):

    layout  = json.loads(open(f, "r").read())
    path    = json.loads(open(f1, "r").read())

    path["o_base"] = os.path.join(path["base"], f)

    for k in path["in"].keys():
        path["in"][k] = os.path.join(path["base"], path["in"][k])
    for k in path["out"].keys():
        path["out"][k] = os.path.join(path["o_base"], path["out"][k])
    # # DEBUG
    # print json.dumps(path, sort_keys=True, indent=4 * ' ')

    # time-stamp and stow away an existing experiment directory

    if os.path.exists(path["o_base"]):
        os.rename(path["o_base"], 
                  os.path.join(path["in"]["attic"], 
                               f + "-" + str(time.time())))
    os.mkdir(path["o_base"])
    for k in path["out"].keys():
        os.mkdir(path["out"][k])

    # flatten the path dict
    path.update(dict(path["in"].items() + path["out"].items()))
    del(path["in"])
    del(path["out"])
    # # DEBUG
    # print json.dumps(path, sort_keys=True, indent=4 * ' ')

    return layout, path

def run(layout, path):

    matrix = layout["matrix"]
    models = layout["models"]
    stems  = layout["stems"]

    s = SysTerrier(path)

    print
    c = 1
    
    doc = []
    for i in matrix.keys():
        doc.append(matrix[i][0])
    doc = list(set(doc))
    n = len(doc) * len(stems)
    for d in doc:
        d_path = os.path.join(path["doc"], d)
        for j in stems:
            spin("indexing", c, n)
            s.index(d+"."+j, d_path, ["stop", j])
            c+=1

    print
    c = 1
    n = len(matrix.keys()) * len(stems) * len(models)

    for i in matrix.keys():
        d = matrix[i][0]
        t_path = os.path.join(path["topic"], matrix[i][1])
        t = Topics(t_path)
        q = t.query("terrier", "d")
        for j in stems:
            for k in models:
                spin("retrieving", c, n)
                s.retrieve(d+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
                c+=1

    print
    c = 1

    n = len(matrix.keys()) * len(stems) * len(models)
    for i in matrix.keys():
        qrel_path = os.path.join(path["qrel"], matrix[i][2])
        for j in stems:
            for k in models:
                spin("evaluating", c, n)
                s.evaluate(i+"."+j+"."+k, qrel_path)
                c+=1

def main(argv):
    layout, path = init("exp1c", "conf");
    run(layout, path)
    
if __name__ == "__main__":
   main(sys.argv)

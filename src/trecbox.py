import sys, os
import simplejson as json
from SysTerrier import *
from SysIndri import *
from SysLucene import *
from Topics import Topics

def init(f, f1):
    layout  = json.loads(open(f, "r").read())
    path   = json.loads(open(f1, "r").read())

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
                  os.path.join(path["in"]["attic"], f + "-" + str(time.time())))

    # create the output directories

    os.mkdir(path["o_base"])
    for k in path["out"].keys():
        os.mkdir(path["out"][k])

    # remove the the nesting in the path dict

    path.update(dict(path["in"].items() + path["out"].items()))
    del(path["in"])
    del(path["out"])

    # # DEBUG
    # print json.dumps(path, sort_keys=True, indent=4 * ' ')

    return layout, path

def run(opt, layout, path):
    matrix = layout["matrix"]
    models = layout["models"]
    stems  = layout["stems"]
    s = SysTerrier(path)
    if opt == "i":
        doc = []
        for i in matrix.keys():
            doc.append(matrix[i][0])
        doc = list(set(doc))
        for d in doc:
            d_path = os.path.join(path["doc"], d)
            for j in stems:
                s.index(d+"."+j, d_path, ["stop", j])
    elif opt == "r":
        for i in matrix.keys():
            d = matrix[i][0]
            t_path = os.path.join(path["topic"], matrix[i][1])
            t = Topics(t_path)
            q = t.query("terrier", "d")
            for j in stems:
                for k in models:
                    s.retrieve(d+"."+j,  i+"."+j+"."+k, ["stop", j], k, q)
    elif opt == "e":
        for i in matrix.keys():
            qrel_path = os.path.join(path["qrel"], matrix[i][2])
            for j in stems:
                for k in models:
                    s.evaluate(i+"."+j+"."+k, qrel_path)

def main(argv):
    if len(argv) != 2:
        print "usage: python setup.py <i|r|e>"
        sys.exit(0)

    layout, path = init("exp1c", "conf");
    run(argv[1], layout, path)
    
if __name__ == "__main__":
   main(sys.argv)

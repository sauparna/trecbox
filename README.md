exp
===

private distributed evals

systems are objects
document collections are paths
topics are objects
qrels are files

Two files, conf and expXYZ encodes the paths and experiment layout in
JSON.

Typically, call init() and run() one after the other.

layout, path = init(expXYZ, conf)
run(opt, layout, path)

The file name 'expXYZ' is also the output directory name for that
experiment. If one exists already, it is time-stamped and moved to the
attic. A fresh directory-tree is planted where all retrieval and eval
output go.

     expXYZ
       |
     ------
    |      |
   run    eval

topic
 data:
  topic - file
  mode - type of query processing
 func:
  query() - constructs a query out of the topic

stop and stem is passed as as a pair of strings in a list ["stopfile", "stemmer"]

stopfile names a file in env["utils"] dir, and stemmer names a
stemmer. Use "None" to skip to exclude stopping or stemming.

conf
====

The configuration file is a JSON, that lays out the paths for the 'in'
and 'out' directories. 'in' defines those directories that are not
created at the time of running an experiment using trecbox. 'out' are
the places where the output files of the experiment go. However, the
'index' directory is sort of both 'in' and 'out' by nature. Since
trecbox keeps indexes at 'base' and not 'o_base' and does not
re-create one if it exists, 'index' is placed amongst the 'in'
paths. trecbox does create an index the first time it encounters one
and places it in base/index.

conf is seeded with the base path and init() constructs paths and
updates the rest of the values. And before passing it onto index(),
retrieve() or evaluate() it flattens it out to a linear key-val dict.

layout
====

The JSON below is a typical experiment layout.

'topic' is a ":"-separated, 3-part string. The first two parts is the
topic file name and the topic part to use (a combination of 't', 'd'
and 'n'). The third part is optional. It is the file name of a list of
qids to use from the list of topics.

{
	matrix: runix: [doc, topic, qrel],
	models: ["model1", "model2", ..., "modelN"],
	stems: ["stemmer1", "stemmer2", ..., "stemmerN"],
	system: ["sysA"]
}

A sample layout:

{"matrix": {"ziff1":   ["ziff12",     "1-100:d:1-100.1.30",      "1-100.cd12"],
	    "ziff2":   ["ziff12",     "1-100:d:1-100.2.30",      "1-100.cd12"],
	    "t678-fr": ["cd45-cr-fr", "301-450:d:301-450-fr.30", "301-450.cd45-cr-fr"],
	    "fr":      ["fr94",       "301-450:d:301-450.fr.30", "301-450.cd45-cr"],
	    "t678a":   ["cd45-cr",    "301-450:d:301-450.a.30",  "301-450.cd45-cr"],
	    "t678b":   ["cd45-cr",    "301-450:d:301-450.b.30",  "301-450.cd45-cr"],
	    "t678c":   ["cd45-cr",    "301-450:d:301-450.c.30",  "301-450.cd45-cr"]
	   },
 "models": ["bm25", "dfi0", "dirichletlm", "lemurtf_idf", "tf_idf"],
 "stems" : ["n", "p"],
 "system": "terrier",
}

analysis
====


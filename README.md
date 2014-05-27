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
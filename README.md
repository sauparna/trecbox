exp
===

private distributed evals

systems are objects
document collections are paths
topics are objects
qrels are files

Two files, conf and expXYZ encodes the paths and experiment layout in
JSON. Typically, call init() and run() one after the other.

layout, path = init(expXYZ, conf)
run(opt, layout, path)

The file name 'expXYZ' is also the output directory name for that
experiment. If one exists already, it is time-stamped and moved to the
attic. A fresh directory-tree is planted where all indexing, retrieval
and eval output go.

    expXYZ
       |
 -------------
|      |      |
index  run    eval

topic
 data:
  topic - file
  mode - type of query processing
 func:
  query() - constructs a query out of the topic

stop and stem is passed as as a pair of strings in a list ["stopfile", "stemmer"]

stopfile names a file in env["utils"] dir, and stemmer names a
stemmer. Use "None" to skip to exclude stopping or stemming.
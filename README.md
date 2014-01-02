exp
===

private distributed evals

systems are objects
document collections are paths
topics are objects
qrels are files

index(), retrieve() and evaluate() overwrites previous data
SysTerrier.index() takes care to move an existing index to the attic
TODO: this asymmetry could be resolved.

topic
 data:
  topic - file
  mode - type of query processing
 func:
  query() - constructs a query out of the topic

stop and stem is passed as as a pair of strings in a list ["stopfile", "stemmer"]

stopfile names a file in env["utils"] dir, and stemmer names a
stemmer. Use "None" to skip to exclude stopping or stemming.
*trecbox* is not a search engine, but a tool that provides an
abstraction for specifying the index-retrieve-evaluate pipeline of a
typical IR experiment. It drives other search systems on TREC data to
this specification.

The input to *trecbox* are two configuration files (in JSON) that
configure the tool and the experiment pipeline. The files have to be
hand-crafted, and their details are described later.

##### USAGE

```python3 trecbox.py <conf> <map>```

'conf' points trecbox to the the retrieval system and the directories
where to put the experiment's output. The 'map' lays out the
experiment. It specifies the systems, test collections and the parts
of the index-retrieve-eval pipeline to engage. The 'map' becomes a
blue-print and record of the experimental set-up. *trecbox* takes care
of generating unique, meaningful names for the index, runs and evals.

##### Organizing the experiment

###### The directory tree

Here is a typical set up that *trecbox* uses.

```
x/
├── ...
├── trec_eval.9.0
├── lucene.TREC
├── terrier.TREC
├── X
│   ├── 0
│   │   ├── doc
│   │   │   └── CD45
│   │   ├── query
│   │   │   ├── t7.50
│   │   │   └── 351-400
│   │   ├── qrel
│   │   │   └── 351-400.cd45-cr
│   │   ├── misc
│   │   │   └── ser17
│   │   ├── index
│   │   │   ├── CD45.017.s
│   │   │   ├── CD45.017.s.docs
│   │   │   └── CD45.017.s.log
│   │   ├── runs
│   │   │   ├── T7.017.s.tfidf.50.T.x
│   │   │   └── T7.017.s.tfidf.50.T.bo1
│   │   └── evals
│   │       ├── T7.017.s.tfidf.50.T.x
│   │       └── T7.017.s.bm25.50.T.bo1
│   ├── maps
│   │   └── 0
│   └── ...
└── ...

```

- `trec_eval.9.0` is the evaluation tool.

- `lucene.TREC` is a mod of Lucene 5.3.1 that works on TREC data.

- `terrier.TREC` is a mod of Terrier 4.0 that works on TREC data.

- `/x/X` is the experiment directory within which experiments' data live.

- `/x/X/0` is one such experiment, and it has to have the hierarchy shown.

- `/x/X/maps` contains the 'map' files that describe an
  experiment. *trecbox* expects that a directory, of the same name as
  the 'map' file's name, exists in `X`. This helps organize an
  experiment neatly and use the corresponding 'map' file as a
  blue-print of the experiment.

- 'doc', 'query', and 'qrel' and 'misc' should contain the
  test-collections. The files/directories speciefied in the 'map' has
  to match these file/directory names. 'misc' usually contains the
  files containing the stop-words.

- 'index', 'runs', 'evals', must be empty at the start but will end up
  with the index, runs and evals once the experiment finishes.

###### 'conf' - Configuring the tool

```
{
"TRECEVAL": "/x/trec_eval.9.0",
"LUCENE"  : "/x/lucene.TREC",
"TERRIER" : "/x/terrier.TREC",
"LEMUR"   : "/x/indri",
"EXP"     : "/x/X",
"DOC"     : "doc",
"QUERY"   : "query",
"QREL"    : "qrel",
"MISC"	  : "misc",
"INDEX"   : "index",
"RUNS"    : "runs",
"EVALS"   : "evals"
}
```

###### '0' - Making the experiment's blue-print

This is what a 'map' looks like and the next block explains the
strings in their positions.

```
{"matrix": {"T7":   ["CD45",    "351-400:T:t7.50",    "351-400.cd45-cr"]
	   },
 "models": ["tfidf:", "bm25:"],
 "stems" : ["s"],
 "stops" : ["ser17"],
 "qexp"  : ["", "bo1:10:3"],
 "system": "terrier"
}
```

```
{"matrix": {<name>: [<doc directory>, <query file>:<T|D|N>:<qid>, <qrel file>]},
 "models": [<model>, ...],
 "stems" : [<stemmer>, ...],
 "stops" : [<stop-words file>],
 "qexp"  : [<>, <qexp name>:<param 1>:<param 2>],
 "system": "terrier"
}
```

- `<name>` is a reasonable name that the test collection needs to be
given.

- `<T|D|N>` specifies the portion of the query to use; the TITLE,
DESCRIPTION or NARRATIVE. Any combination of these three characters
mean that all those parts are to be concatenated and treated as one
query.

- `<qid>` is a file listing the query IDs to be used. It is a way to
  use a subset of the queries if necessary.

- `<model>`, `<stemmer>` are names of models and stemmers to be
used. These depend on the the retrieval system being used.

- `<qexp names>` specifies what 'query expansion' algorithm to use. This
depends on the retrieval system, and how the system names these
intricacies. It so happens that one of Terrier 4.0's query exapnsion
algorithms needs two other parameters, which can be specified in the
'map' as `<param 1>` and `<param 2>`.

- `""` The empty double-quote specifies that no query expansion is to be
used. This way, stopping and stemming could also be switched off. Of
course, using it in `matrix` makes no sense.

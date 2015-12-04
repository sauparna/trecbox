*trecbox* is not a search engine, but a tool that provides an
abstraction for specifying the index-retrieve-evaluate pipeline of a
typical IR experiment. It drives other search systems on TREC data
following this specification.

The input to *trecbox* are two hand-crafted configuration files (in
JSON) that configure the tool and the experiment's pipeline.

##### USAGE

```python3 trecbox.py <conf> <map>```

'conf' points trecbox to the the retrieval system and the directories
where to put the experiment's output. 'map' specifies the systems,
test collections and the parts of the index-retrieve-eval pipeline to
engage. The 'map' file becomes a blue-print of the experiment.

Here is an example of an experimental setup showing a 'conf', a 'map',
a directory tree and files. `x/X` is the experiment's directory and an
experiment whose blue-print is written in a file named, `x/maps/Y`,
must have a directory named `Y` in `X`. The seven sub-directories of
`Y` must be created at the outset, and, `doc`, `query`, `qrel` and
`misc` populated with the relevant files mentioned in `Y`. `index`,
`runs`, `evals` is left empty and gets populated with the output when
*trecbox* finishes running an experiment.

*trecbox* helps to make sure an experiment is documented (in the file
 `Y`), organized neatly (in the directory `X/Y`) and therefore, easily
 reproducible.

It saves space to use symbolic links to the the data, especially in
`Y/doc`, instead of copying everything into each experiment that you
design.

###### Where everything stays:

```
x/
├── ...
├── trec_eval.9.0
├── lucene.TREC
├── terrier.TREC
├── indri
├── X
│   ├── Y
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
│   │   └── Y
│   └── ...
└── ...
```

###### conf

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

###### `Y`
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

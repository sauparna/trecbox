[trecbox][trb] is not a search engine, but a tool that provides an
abstraction for specifying the index-retrieve-evaluate pipeline of a
typical IR experiment. It drives other search systems on TREC data
following this specification. This helps organize an experiment neatly
and easy to reproduce later.

A hypothetical layout of the input and output data is shown. The
configuration files passed to *trecbox* point to these resources. Note
how the experiment-directory X contains the experiment-layout in a
file Y in X/maps and the experiment is encapsulated in a directory of
the same name Y in X.

##### Prerequisites

+ Python 3
+ simplejson
+ lxml
+ beautifulsoup4

##### Usage

```python trecbox.py <conf> <Y>```

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
{"matrix": {"T7": ["CD45", "351-400:T:t7.50", "351-400.cd45-cr"]},
 "models": ["tfidf:", "bm25:"],
 "stems" : ["s"],
 "stops" : ["ser17"],
 "qexp"  : ["", "bo1:10:3"],
 "system": "terrier"
}
```

###### Data

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

[trb]: http://scarlet.freeshell.net/ir/trecbox

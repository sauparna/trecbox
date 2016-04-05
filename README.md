**trecbox** is not a search engine, but a tool that provides an
abstraction for specifying the index-retrieve-evaluate pipeline of a
typical IR experiment. It drives other search systems on TREC data
following this specification.

A hypothetical layout of the input and output data is shown. The
configuration files passed to trecbox point to these resources. Note
that in the experiment-directory the experiment-map is in a file at
*/x/Experiments/maps/Y* and the experiment is encapsulated in a
directory at */x/Experiments/Y/*.

[Documentation][trb]

##### Prerequisites

+ Python 3
+ Python libraries:
  - simplejson
  - lxml
  - beautifulsoup4

##### Usage

```python trecbox.py X Y
```

##### X

```
{
"TRECEVAL": "/x/trec_eval.9.0",
"LUCENE"  : "/x/LTR",
"TERRIER" : "/x/TTR",
"LEMUR"   : "/x/indri",
}
```

##### Y

```
{"testcol": {"T7": ["CD45", "351-400:T:t7.50", "351-400.cd45-cr"]},
 "models" : ["tfidf", "bm25"],
 "stems"  : ["s"],
 "stops"  : ["ser17"],
 "qexp"   : ["", "bo1:10:3"],
 "system" : "terrier"
}
```

###### Locations

```
x/
├── ...
├── trec_eval.9.0
├── LTR
├── TTR
├── indri
├── Experiments
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
│   │   │   ├── CD45.a.s
│   │   │   └── CD45.a.s.docs
│   │   ├── runs
│   │   │   ├── T7.a.s.tfidf.50.T.x
│   │   │   └── T7.a.s.tfidf.50.T.bo1
│   │   ├── evals
│   │   │   ├── T7.a.s.tfidf.50.T.x
│   │   │   └── T7.a.s.tfidf.50.T.bo1
│   │   └── log
│   │       ├── *.i
│   │       ├── *.r
│   │       └── *.e
│   ├── maps
│   │   └── Y
│   └── ...
└── ...
```

[trb]: http://kak.tx0.org/IR/trecbox

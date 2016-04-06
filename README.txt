*******
TRECBOX
*******

Rup Palchowdhury
rup.palchowdhury[at]gmail.com

This is a tool that provides an abstraction for specifying the
index-retrieve-evaluate pipeline of a typical IR experiment. It drives
other search systems on TREC data. The purpose and utility of it is
discussed in this write-up: http://kak.tx0.org/IR/trecbox.

----------------------------------------------------------------------

TABLE OF CONTENTS

A. PREREQUISITES

B. IR EXPERIMENTS

   1. SETTINGS FILE FORMAT

   2. SPECIFICATION FILE FORMAT

----------------------------------------------------------------------

A. PREREQUISITES

Python 3
Python libraries:
	lxml
	beautifulsoup4

----------------------------------------------------------------------

B. IR EXPERIMENTS

An experiment is run by typing this at the shell:

   trecbox.py [settings] [spec]

In the settings file are the locations of the search systems and the
output directory. A specification of the experiment pipeline is read
from the spec file and translated to appropriate configuration
parameters which the systems understand. Depending on what the target
system needs, the configuration is either written to another file or
passed as command line options. The target system's binaries are
executed using Python's subprocess module.

----------------------------------------------------------------------

1. SETTINGS FILE FORMAT

See settings.txt for a sample. The paths in the sample are imaginary,
they need to be changed to point to actual locations in a file system.

This is of the following form:

    EVAL /x/trec_eval.9.0
    LUCENE /x/Lucene
    TERRIER /x/Terrier
    LEMUR /x/Indri
    EXP /x/Y

Where the settings are

    EVAL - Evaluation program's directory.

    LUCENE, TERRIER, LEMUR - Installation directories of search
    systems.

    EXP - Directory where experiments' output go. A directory of the
    same name as the spec file has to be created below it and several
    subdirectories created inside that as placeholders for the input
    and output files. The directory tree is as shown below:

                      [EXP] 
                        |
                   --------------
                  |       |      |
                spec1*  spec2*  ...
                  |       |
		  |      ...
		  |
     ------------------------------------------------
    |      |      |     |     |      |    |     |    |
   doc*  query*  qrel*  misc*  index  runs  evals  log


    * Must be created and populated before running trecbox.

    doc - Must contain a single directory within which the corpus is
    kept. The corpus may be symlinks to the data located elsewhere on
    the file system.

    query - Contains the TREC query files.

    qrel - The TREC qrel files are in here, along with plain text
    files containing lists of query IDs (one per line) specifying the
    subset of queries that are to be used in the experiment.

    misc - The stop word files are placed here.

    index, runs, evals - Have the output/results of the various stages
    of the experiment.

    log - This will contain dumps of stdout and stderr of the invoked
    processes. The log files end in .i, .r and .e; corresponding to
    the indexing, retrieval and evaluations stages of the pipeline.

----------------------------------------------------------------------

2. SPECIFICATION FILE FORMAT

See spec.txt for a sample. The format is similar to the settings
file. (Note that, in the sample, variables have be repeated for better
readability, otherwise, specifying a large number of models on one
line looks clumsy.)

This is of the follwoing from:

    TESTCOL [name] [doc] [query:part:subset] [qrel]
    MODEL [m1] [m2] ...
    STEM [s1] [s2] ...
    STOP [p1] [p2] ...
    QEXP [x1] [x2] ...
    SYS [sys]

Where a variables on the left specify a type of parameter and is
followd by a space-separated list of actual parameter values.

    TESTCOL - Specifies a name and the three components of a TREC
    test-collection; documents, queries and qrels.

        [name] - A string used to identify the test-collection.
 
	[doc] - The name of the directory in the 'doc' directory (see
	'SETTINGS FILE').

	[query:part:subset] - 'query' is the query file, 'part' is a
 	string constructed from a combination of the elements of the
 	set of characters {T, D, N}, to specify the parts of a query
 	to use; the Title, Description or Narrative or a combination
 	of them. 'subset' is a file containig a subset of the query
 	IDs of the queries in the 'query' file for that experiment.

 	[qrel] - The TREC qrel file.

    MODEL, STEM, STOP, QEXP, SYS - Specify the pieces of an IR
    experiment. The space-separated strings ([m1], [p2], [sys] and so
    on) are picked from a vocabulary specific to each search
    system. (See 'VOCABULARY' in following sections.)

----------------------------------------------------------------------

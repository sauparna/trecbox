*******
TRECBOX
*******

Rup Palchowdhury
rup.palchowdhury[at]gmail.com

This is a tool that provides an abstraction for specifying the
index-retrieve-evaluate pipeline of a typical IR experiment. It drives
other search systems on TREC data. The putpose and utility of such a
tool is discussed at http://kak.tx0.org/IR/trecbox.

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
output directory. It reads a specification of the experiment pipeline
from the spec file and translates them to appropriate configuration
parameters which the systems understand. Depending on what the target
system needs, the configuration is either written to another file or
passed as command line options. The target system's binaries are
executed using Python's subprocess module.

----------------------------------------------------------------------

1. SETTINGS FILE FORMAT

See settings.txt for a sample. The paths in the sample are imaginary,
they need to be changed to point to actual locations in a file system.

This is of the following form:

    [var] [path]

Where the [var] belongs to the set of strings:

    {EVAL, LUCENE, TERRIER, LEMUR, EXP}

and is followed by a [path] to a directory.

    EVAL - Points to the evaluation program's directory.

    LUCENE, TERRIER, LEMUR - Point to the installation directories of
    those search systems.

    EXP - Is the directory where each experiment's output will be
    written. A directory of the same name as the spec file has to be
    created below it and several subdirectories created inside that,
    where in some, the input files are to be placed by hand while the
    others are placeholders for the experiment's output files. The
    directory tree is as shown below:

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
    kept. The corpus may be a collection of files, directories or
    both, or even symlinks to the data located elsewhere on the file
    system.

    query - The TREC query files are place here.

    qrel - The TREC qrel files are placed here, along with plain text
    files containing lists of query IDs (one per line) specifying the
    subset of queries are to be used in the experiment.

    misc - The stop word files are placed here.

    index, runs, evals - The output/results of the various stages of
    the experiment go here.

    log - This will contain dumps of the stdout and stderr of the
    invoked search systems to be used for debugging purposes later.

----------------------------------------------------------------------

2. SPECIFICATION FILE FORMAT

See spec.txt for a sample. The format is similar to the settings
file. (Note that, in the sample, variables have be repeated for better
readability, otherwise, specifying a large number of models on one
line looks clumsy.)

This is of the follwoing from:

    [var] [v1] [v2] ...
    TESTCOL [name] [doc] [query:part:subset] [qrel]
    SYS [s1]

Where a variable [var] specifies a type of parameter and is followd by
a space-separated list of actual parameter values. The TESTCOL and SYS
variables have been singled out because they have a different format
and meaning.

    [var] - This has to be one from the the following set of strings:
    {MODEL, STEM, STOP, QEXP, SYS}. All of them have to be specified,
    each on a new line. Each of [v1], [v2], ... and so one, are string
    from a vocabulary specific to a search system. The 'Vocabulary'
    section list the all of them for each system.

    TESTCOL - Specifies the three components that constitutes an TREC
    test-collection; documents, queries and qrels.

        [name] - A string used to identify the test-collection.
 
	[doc] - The name of the directory in the 'doc' directory (see
	'SETTINGS FILE').

	[query:part:subset] - 'query' is the query file name, 'part'
 	is a string constructed from a combination of the elements of
 	the set of characters {T, D, N}, to specify which parts of the
 	quries to use; the Title, Description or Narrative or some
 	combination of them. 'subset' is a file containig alist of
 	query IDs to pick a subset of the queries in the 'query' file
 	for the experiment if the need be.

 	[qre] - The qrel file.

    SYS - Is one of the string {terrier, lucene, indri}.

----------------------------------------------------------------------

TRECBOX

Rup Palchowdhury
rup.palchowdhury[at]gmail.com

(C) Copyright 2013-2016, Rup Palchowdhury

This is free software, you can redistribute it and/or modify it under
the terms of the GNU General Public License.

The GNU General Public License does not permit this software to be
redistributed in proprietary programs.

This software is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

----------------------------------------------------------------------
DESCRIPTION

This is a tool that provides an abstraction for specifying the
index-retrieve-evaluate pipeline of a typical IR experiment. It drives
other search systems on TREC data.

----------------------------------------------------------------------
TABLE OF CONTENTS

A. PREREQUISITES

B. IR EXPERIMENTS

   1. SETTINGS FILE FORMAT

   2. SPECIFICATION FILE FORMAT

C. NAMING

D. VOCABULARY

E. PRE-PROCESSING TREC QUERIES

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
    sub-directories created inside that as placeholders for the input
    and output files. The directory tree is as shown below:

                      [EXP] 
                        |
                   --------------
                  |       |      |
                spec1*  spec2*  ...
                  |       |
		  |      ...
		  |
     ----------------------------------------------
    |      |      |      |       |     |     |     | 
   doc*  query*  qrel*  misc*  index  runs  evals  log


    *Must be created and populated before running trecbox.

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

This is of the following from:

    TESTCOL [name] [doc] [query:part:subset] [qrel]
    MODEL [m1:c1] [m2:c2] ...
    STEM [s1] [s2] ...
    STOP [p1] [p2] ...
    QEXP [x1:t1:t2] ...
    SYS [sys]

Where a variables on the left specify a type of parameter and is
followed by a space-separated list of actual parameter values.

    TESTCOL - Specifies a name and the three components of a TREC
    test-collection; documents, queries and qrels.

        [name] - A string used to identify the test-collection.
 
	[doc] - The name of the directory in the 'doc' directory (see
	'SETTINGS FILE').

	[query:part:subset] - 'query' is the query file, 'part' is a
 	string constructed from a combination of the elements of the
 	set of characters {T, D, N}, to specify the parts of a query
 	to use; the Title, Description or Narrative or a combination
 	of them. 'subset' is a file containing a subset of the query
 	IDs of the queries in the 'query' file for that experiment.

 	[qrel] - The TREC qrel file.

    MODEL - Retrieval algorithm details.

	[m1] - Name of the retrieval model (e.g. BM25)
	
	[c1] - A constant parameter for an algorithm. (Terrier
	requires such a thing, see
	http://kak.tx0.org/IR/TTR/Doc/Heuristics for a table of
	values.)
    
    STEM, STOP, SYS - Specify the pieces of an IR experiment. The
    space-separated strings ([s1], [p2], [sys] etc.) are picked from a
    vocabulary specific to each search system. (See 'VOCABULARY' in
    the following sections)

    QEXP - Types of query expansion and associated parameters.

        [x1] - The name of the query-expansion algorithm.

	[t1], [t2] - Two parameters for the algorithm (for Terrier).

----------------------------------------------------------------------
C. NAMING

Directories containing the index within the 'index' directory have the
following naming scheme:

    [name].[stop].[stem]

Where [name] is the string '[name]' from the TESTCOL specification in
the spec file, [stop] and [stem] are the names for the stop word file
and the stemmer.

Run files and eval files have identical names (they reside in separate
directories) and their scheme is as follows:
  
    [name].[stop].[stem].[model].[query count].[query part].[qexp]


The first three strings match the index name, the rest are
self-explanatory.

The character 'x' in a name denotes the absence of that stage in the
pipeline.

----------------------------------------------------------------------
D. VOCABULARY

This table maps the different strings used for spec file variables to systems. 

Key:

*Blanks in the table imply that there are no corresponding concept.
*The character 'x' denotes the absence of a specification.

SPEC - Strings that are used in the spec file

NAME - Counterparts of spec file strings used in naming indexes, runs
and evals (See NAMING section). Strings from the spec were shortened
to single characters to avoid long output file names.

LUCENE, TERRIER - Counterparts of spec file names in the system's
context.

Stop Words
----------------------------------------------------------------------
    SPEC          NAME LUCENE                   TERRIER
----------------------------------------------------------------------
    ser17         a    ser17                    ser17
    lucene33      b    lucene33                 lucene33
    indri418      c    indri418                 indri418
    smart571      d    smart571                 smart571
    terrier733    e    terrier733               terrier733
    x             x    x                        x

Stemmers
----------------------------------------------------------------------
    SPEC          NAME LUCENE                   TERRIER
----------------------------------------------------------------------
    Porter        p    PorterStemFilter	        PorterStemmer
    Weak Porter   w                             WeakPorterStemmer
    Krovetz       k    KStemFilter              
    Snowball      o    SnowballFilter           EnglishSnowballStemmer
    S-Stemmer     s    EnglishMinimalStemFilter SStemmer
    x             x

Query Expansion Algorithms
----------------------------------------------------------------------
    SPEC          NAME LUCENE                   TERRIER
----------------------------------------------------------------------
    kl            kl0                           KL
    klapprox      kla                           BA
    klinformation kli                           Information
    klcomplete    klm                           KLComplete
    klcorrect     klr                           KLCorrect
    bo1           bo1                           Bo1
    bo2           bo2                           Bo2
    x		  x

Retrieval Models
----------------------------------------------------------------------

The full list of models in each system, their names and what they mean
is gathered on these pages:

Lucene
https://github.com/sauparna/LTR/blob/master/mods/models.lucene

Terrier
https://github.com/sauparna/TTR/blob/master/mods/models.terrier

TF-IDF Repository
http://kak.tx0.org/IR/TF-IDF

----------------------------------------------------------------------
E.  PRE-PROCESSING TREC QUERIES

This is what the pre-processed TREC query looks like:

    <TOP>
     <NUM>301</NUM>
     <TEXT>
        Why is a raven like a writing-desk?
     </TEXT>
    <TOP>

Here is a snippet of code to test the query parser:

    import sys, os
    from Query import Query

    q = Query(query_file, "TD", query_subset_list, "lucene")
    q.parse()
    t = q.write_xml(out_dir, out_file)


'q' is a Python OrderedDict, returned by _query()_, of the form;

    {301: "why is a raven like a writing-desk?"}

The parts of the query (Title and Description, "TD", here) are
concatenated and placed within the <TEXT> tags. The systems are rigged
to read this formatting and not worry about picking the query-parts.

----------------------------------------------------------------------

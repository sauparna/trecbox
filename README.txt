TRECBOX

Rup Palchowdhury
rup.palchowdhury [at] gmail [dot] com

MIT License

Copyright (c) 2016 Rup Palchowdhury

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

----------------------------------------------------------------------
DESCRIPTION

This is a tool that provides an abstraction for specifying the
index-retrieve-evaluate pipeline of a typical IR experiment. It drives
other search systems on TREC data.

----------------------------------------------------------------------
TABLE OF CONTENTS

A.  PREREQUISITES

A1. WINDOWS SETUP

B.  IR EXPERIMENTS

    1. SETTINGS FILE FORMAT

    2. SPECIFICATION FILE FORMAT

C.  NAMING

D.  VOCABULARY

E.  PRE-PROCESSING TREC QUERIES

----------------------------------------------------------------------
A. PREREQUISITES

Python 3
Python libraries:
    lxml
    beautifulsoup4

----------------------------------------------------------------------
A1. WINDOWS SETUP

1. Run package installations like 'pip install' in a cmd
   'Administrator' window:

    right click cmd icon -> move mouse to move selection to 'Command Prompt' in the pop-up menu -> right click -> chose 'Run as administrator'

2. Compile a trec_eval exe for Windows
   (https://github.com/usnistgov/trec_eval):

   To achieve a compilation of trec_eval for Windows, you will need
   Cygwin installed. Download and install the Cygwin platform. You
   will need make and gcc installed by Cygwin. To achieve this, on top
   of the default Cygwin installation, it is recommended to install
   automake, make, gcc, cygwin-gcc and git from the Develop category,
   and permitting dependencies to be installed. Then, to compile
   trec_eval, open a Cygwin Terminal, navigate using cd to the
   directory of the trec_eval source, and type make.

   The resulting trec_eval.exe should be usable directly from the
   Cygwin Terminal. The resulting trec_eval.exe should be usable on
   any machine without Cygwin installed, as long as the cygwin1.dll is
   available. For instance, place a copy the cygwin1.dll from Cygwin's
   /bin directory into the same directory as trec_eval.exe.

3. Symlinks to a corpus directory from the experiment's 'doc'
   directory is created using the mklink command in the
   'administrator' CLI:

    mklink /D link target

----------------------------------------------------------------------
B. IR EXPERIMENTS

An experiment is run by typing this at the shell:

   trecbox.py settings.txt exp-ltr.txt

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

    EXP - Directory where the entire experiment lives. A directory of
    the same name as the specification file (i.e. 'exp-ttr' in this
    example) has to be created below it and several sub-directories
    created in 'exp-ttr' as placeholders for the input and output
    files. The directory tree has to be as shown below:

                        Y
                        |
                   -----------------
                  |          |      |
                  |       exp-ttr*  ...
                  |          |
	       exp-ltr*      ...
		  |
     ----------------------------------------------
    |      |      |      |       |     |     |     | 
   doc*  query*  qrel*  misc*  index  runs  evals  log


    * To be created and populated manually before running trecbox.

    doc - Must contain a single directory within which the corpus is
    kept. (Symlinks to a corpus elsewhere on the disk will do.)

    query - Contains the TREC query files and associated files
    containing list of query-IDs to speficy a subset of the queries.

    qrel - The TREC qrel files are in here.

    misc - The stop word files are placed here.

    index, runs, evals - Have the output/results of the various stages
    of the experiment.

    log - This will contain dumps of stdout and stderr of the invoked
    processes. The log files end in .i, .r and .e; corresponding to
    the indexing, retrieval and evaluations stages of the pipeline. A
    .q file has the copy of the pre-processed queries.

----------------------------------------------------------------------
2. SPECIFICATION FILE FORMAT

See exp-ttr.txt for a sample. The format is similar to the settings
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

This table maps the strings used for spec file variables, to
intermediate names or concepts in the systems.

Key:

*Blanks in the table imply that there are no corresponding concept.

*The character 'x' implies 'switching off' of a specification.

*The model names that are common amongst LTR and TTR are listed
 here. For a full list of models avaiable in the sytems, see the
 'models' file in their directories.

SPEC - Strings that are used in the spec file

NAME - Counterparts of concepts used in TRECBOX for using in run tags
(See NAMING section). Since the run tags are used as file names,
strings from the specification were shortened to single characters to
avoid long output file names.

LUCENE, TERRIER - Counterpart of concept names used within the
systems.

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
    x             x                             x

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
    x		  x                             x

Retrieval Models
----------------------------------------------------------------------
    SPEC          NAME LUCENE                   TERRIER
----------------------------------------------------------------------
    bm25          bm25 BM25                     BM25
    tmpl          tmpl TMPL                     TMPL
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


'q' is a Python OrderedDict, returned by query(), of the form;

    {301: "why is a raven like a writing-desk?"}

The parts of the query (Title and Description, "TD", here) are
concatenated and placed within the <TEXT> tags. The systems are rigged
to read this formatting and not worry about picking the query-parts.

----------------------------------------------------------------------

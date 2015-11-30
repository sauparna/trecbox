*trecbox* is a tool to drive other retrieval/evaluation systems on
TREC data and to also help organise an IR exepriment neatly. The input
to trecbox are two plain text files, a configuration and a map. Both
the files have to be written manually, which is explained in detail
later. 'conf' points trecbox to the the retrieval system, and, places
where to put the experiment's output. The output is the 'runs' and the
'evals'. The 'map' file lays out the experiment. It tells trecbox
which system to use, which test collection, and which parts of the
index-retrieve-eval pipeline to engage. Once a map has been written,
it becomes documentation for the entire experiment. trecbox takes care
of generating unique, meaningful names for the index, runs and evals
for easier analysis of the experiment.  An example of how to set up
and use trecbox will make things clear.

###### USAGE

python3 trecbox <conf> <map>

###### conf


###### map


###### system and data location


###### experiment
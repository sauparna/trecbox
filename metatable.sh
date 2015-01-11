# Gathers all the meta tables from meta/tables/*.m into one file.
# USAGE: bash metatable.sh indir outf
indir=$1
outf=$2
cat /dev/null >$outf
for f in tfidf stem noidf nondl nologtf nondl
do
    echo "$f" >>$outf
    cat $indir/$f.m >>$outf
    echo "" >>$outf
done

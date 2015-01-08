# USAGE: meta evaldir outdir
# The output table is: [testcol topi MAP1 MAP2]

# # when pwd is 1/analysis/pairs
# evaldir=../../evals
# outdir=.

evaldir=$1
outdir=$2

echo "testcol topic MAP1 MAP2" >$outdir/tfidf
for t in FBIS FR FT LA T6 T678 T7 T8
do 
    paste $evaldir/$t.n.TFIDF0 $evaldir/$t.p.TFIDF0 | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/tfidf
    paste $evaldir/$t.p.TFIDF0 $evaldir/$t.p.SERSIMPLE | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/tfidf
    paste $evaldir/$t.p.TFIDF0 $evaldir/$t.p.NOIDF | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/tfidf
    paste $evaldir/$t.p.TFIDF0 $evaldir/$t.p.NONDL | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/tfidf
    paste $evaldir/$t.p.TFIDF0 $evaldir/$t.p.NOLOGTF | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/tfidf
    paste $evaldir/$t.p.TFIDF0 $evaldir/$t.p.LOGNDL | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/tfidf
done

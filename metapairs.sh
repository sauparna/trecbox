# USAGE: meta evals outdir
# The output table is: [testcol topic MAP1 MAP2]

evaldir=$1
outdir=$2

while read line
do
    map=( ${map[@]} $line )
done <<EOF
stem:n.TFIDF0:p.TFIDF0
tfidf:p.TFIDF0:p.SERSIMPLE
noidf:p.TFIDF0:p.NOIDF
nondl:p.TFIDF0:p.NONDL
nologtf:p.TFIDF0:p.NOLOGTF
logndl:p.TFIDF0:p.LOGNDL
EOF

for str in "${map[@]}"
do
    OLDIFS=$IFS
    IFS=":";read -a x <<< "$str";IFS=$OLDIFS
    pair="${x[0]}"
    ctrl="${x[1]}"
    tret="${x[2]}"
    echo "testcol topic MAP1 MAP2" >$outdir/$pair;
    for t in FBIS FR FT LA T6 T7 T8 T678
    do
	# echo "$evaldir/$t.$ctrl $evaldir/$t.$tret $outdir/$pair"
	paste $evaldir/$t.$ctrl $evaldir/$t.$tret | awk -v t=$t '$1 ~ /^map/ && $2 !~ /all/{print t " " $2 " " $3 " " $6}' >>$outdir/$pair
    done
done

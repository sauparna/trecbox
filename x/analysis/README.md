usage:
awk -f ../x/analysis/select.awk t678.* | awk -f ../x/analysis/gather.awk | sort -k1,1 >file

The above line selects measures and gathers them by test collection
and writes files in viz. Run it from within evals directory for neater
output.

awk -f table.awk will work on them in viz to get a table out

tab0 in viz is the entire results table without headers
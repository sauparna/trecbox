usage:
awk -f ../x/analysis/select.awk t678.* | awk -f ../x/analysis/gather.awk | sort -k1,1 >file
The above line selects measurs and gathers them by test collection and writes files in viz
awk -f table.awk will work on them in viz to get a table out
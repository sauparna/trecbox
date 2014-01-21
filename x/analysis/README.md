usage:
awk -f ../x/analysis/select.awk t678.* | awk -f ../x/analysis/gather.awk | sort -k1,1 >file

The above line selects measures and gathers them by test collection
and writes files in viz. Run it from within evals directory for neater
output.

awk -f table.awk will work on *.measures in viz to write out a tab0
commenting on / off some lines controls prettyprinting, and jumbling
up the positions of the test collection columns.

awk -f table1.awk produces a rearranged output of the above
commenting on / off some printf()'s controls prettyprinting.

tab in viz is the entire results table without headers (output of table.awk)
tab.1 has the same data as tab, but laid out differently (output of table1.awk)
*.rand.* has the test collection columns randomly ordered
*.pretty are readable versions of tab*
*.pretty-hide is the readable version of *.rand.* with test collection names replaced by alphabets

single-measure tables from tab.1 types
sort -k2,2d tab0.1 | grep map | grep -v gm_map >tab.1.map
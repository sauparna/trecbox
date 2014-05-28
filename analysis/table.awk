# formats evals into a table where a row is composed of the following
# pieces:
#
# testcol stem model map gm_map Rprec P_5 P_10
# t8 p tf_idf 0.1767 0.0534 0.2104 0.4000 0.3667
#
# Usage: awk -f table.awk path/to/evals/*

BEGIN {
    s[""]  = ""
}
{
    # NOTE: the measures are printed in a row from left to right for
    # each run in the order it appears in the eval files. For
    # convenience the regex pattern lists the measure names in that
    # same order.
    
    if ($1 ~ /^(map|gm_map|Rprec|P_5|P_10)$/ && $2 ~ /all/) {
	runid = FILENAME
	sub(/.*\//, "", runid)
	s[runid] = s[runid] $3 " "	    
    }
}
END {
    printf("# %s %s %s %s %s %s %s %s", "testcol", "stem", "model", 
	   "map", "gm_map", "Rprec", "P_5", "P_10")
    for (k in s) {
	n = split(k, a, /\./)
	for (i=1; i<=n; i++)
	    printf("%s ", a[i])
	printf("%s\n", s[k])
    }
}
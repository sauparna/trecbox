# prettyfies tables
# Usage: awk -f pretty.awk tab
BEGIN {
}
{
    for (i=1; i<=NF; i++) {
	if(i == 1 && NR != 1)
	    $i = substr($i, 1, 4);
	printf("%-7s ", $i)
    }
    printf("\n")
}
END {
}
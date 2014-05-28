# prettyfies tables
# Usage: awk -f pretty.awk tab
BEGIN {
}
{
    for (i=1; i<=NF; i++) {
	if(i == 1) {
	    $i = substr($i, 1, 10);
	    printf("%-10s ", $i)
	}
	else
	    printf("%-7s ", $i)
    }
    printf("\n")
}
END {
}
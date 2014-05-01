BEGIN {
   c = 0
   s[""] = ""
}
{
    if ($1 ~ /^(map|Rprec|P_10|P_5|gm_map)/ && $2 ~ /all/) {
	s[FILENAME] = s[FILENAME] $1 ":" $3 " "
    }
}
END {
    for (f in s) {
	print f " " s[f]
    }
}
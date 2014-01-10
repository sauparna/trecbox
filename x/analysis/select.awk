# select specific measures
{
     if($0 ~ /^(map|Rprec|P_10 |P_5 |gm_map).*all/)
	  print FILENAME " " $1 " " $3
}
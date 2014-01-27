# runs through a tab0.1.*.<measure> type, diffing the values across stemmers
BEGIN{
     f = "../../viz/tab.1.rand.map"
     c = 0
     e = 1.0e-20
     
     while(getline <f)
     {
	  s = ""
	  c++
	  n = NF - 3

	  if (c == 1)
	  {
	       for (i=4; i<=NF; i++)
	       {
		    v[i-3] = $i
		    s = s sprintf("%8.4f", $i)
	       }
	       printf("%-3s%-12s%4s%s\n", $1, $2, $3, s)
	       continue
	  }
	  
	  for (i=4; i<=NF; i++)
	  {
	       diff = ($i - v[i-3] + e)/(v[i-3] + e) * 100.0
	       s = s sprintf("%+8d", diff)
	       # diff = $i - v[i-3]
	       # s = s sprintf("%+8.4f", diff)
	  }
	  printf("%-3s%-12s%4s%s\n", $1, $2, "", s)

	  if (c == 4)
	  {
	       printf("\n")
	       c = 0
	  }
     }
}

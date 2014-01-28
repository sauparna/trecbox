# Writes out the same data as table.awk does, but rearranges the
# measures to go on each line instead of being juxtaposed. It can be
# used to print any number of the measures.
#
# For N test collections, a line of output looks like this:
# rtag measure val1 val2 ... valN

BEGIN{

     if (ARGC != 3)
     {
	  print "Usage: awk -f table1.awk <measures> <file>"
	  print "measures is the list of measures separated by commas with no space between them"
	  print "use the following strings: map, gm_map, Rprec, P_5, P_10"
	  print "e.g. awk -f table1.awk map,Rprec,P_5 tab"
	  print "e.g. awk -f table1.awk map,gm_map,Rprec,P_5,P_10 tab.rand"
	  exit
     }
	  
     f = ARGV[2]
     measures = ARGV[1]
     N_ = split(measures, m, ",")

     # setup the starting indeces of the fields of the five measures
     str = "map gm_map Rprec P_5 P_10"
     N = split(str, m_, " ")
     for (i=1; i<=N; i++)
	  m_i[m_[i]] = i + 1
     
     s = ""
     while(getline <f)
     {
	  rtag = $1

	  # decoupling the stemmer marker from the model makes awking
	  # or sorting this file easier later
	  gsub("[.]", " ", rtag)
	  split(rtag, r, " ")

	  for (i = 1; i <= N_; i++)
	  {
	       # m[i] is a measure string, m_i[] holds the start indeces
	       #
	       # hop in steps of 5 across a line, picking the measure
	       # values and string it together in s

	       for (j = m_i[m[i]]; j <= NF; j += 5)
		    s = s " " $j
	       printf("%-2s %-11s %6s%s\n", r[1], r[2],  m[i], s)
	       s = ""
	  }
     }
}
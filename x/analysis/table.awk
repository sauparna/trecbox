# prints all 5 measures for all 84 systems for all 7 test collections
# NOTE: the above figures may change

#t678.n.bb2  map:0.1531 gm_map:0.0413 Rprec:0.1966 P_5:0.3640 P_10:0.3260

BEGIN {
     getline root <"../config"
     names = "t678 t678-fr t6 t7 t8 fbis fr94"
     # names = "t678 t678-fr"
     measures = "map gm_map Rprec P_5 P_10"

     L = 5 # number of measures
     M = 3 # number of systems, also the number of lines in each file
     N = 7 # number of test collections

     if(split(names, f, " ") != N) {
	  print "Error: number of files != N"
	  exit
     }

     if(split(measures, g, " ") != L) {
	  print "Error: number of files != L"
	  exit
     }

     # format a table header

     # L floating point values each 6 chars long, with L - 1 spaces
     # between them, plus 2 white spaces separating test collection
     # blocks, plus one more white space that 

     w = L * 6 + (L - 1) + 2

     fmt = "%-20s"

     # build the test collection header
     h1 = sprintf(fmt, "sys")
     for (i=1; i <= N; i++)
     {
	  fmt_ = "%-" w "s"
	  h1 = h1 sprintf(fmt_, f[i])
     }
     h1 = h1 sprintf("\n")

     # built the measures header
     h2 = sprintf(fmt, "measures:")
     for (i=1; i <= N; i++)
     {
     	  for (j=1; j <= L; j++)
     	  {
     	       h2 = h2 sprintf("%-6s ", g[j])
     	  }
     	  h2 = h2 sprintf(" ")
     }
     h2 = h2 sprintf("\n")

     # write out neat headers
     printf(h1)
     printf(h2)
     
     for (i=1; i <= M; i++)
     {
	  s["dummy"] = ""
     	  for (j=1; j <= N; j++)
	  {
	       v = ""
	       f_ = "../../viz/" f[j] ".measures"
     	       getline a[j] <f_

	       split(a[j], a_, " ")

	       # erase a part of the rtag
      
	       gsub(f[j] ".", "", a_[1])

	       # clean up the values

	       for (k=2; k <= L+1; k++)
	       {
	       	    split(a_[k], a__, ":")
	       	    v = v " " a__[2]
	       }

	       gsub(/^[ ]*/, "", v)
	       s[a_[1]] = s[a_[1]] "  " v
     	  }
	  gsub(/^[ ]*/, "", s[a_[1]])
	  printf("%-20s%s\n", a_[1], s[a_[1]])
	  delete s
     }
}

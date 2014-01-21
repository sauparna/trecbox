# Usage: awk -f table.awk 
# Run the script from inside x/analysis/ directory. TODO: clean this up
# prints all 5 measures for all 84 systems for all 7 test collections
# NOTE: the above figures may change
#
# A line of output is of the form:
#
# rtag measure1:val1 measure2:val2 ... (more such in sets of 5, each
# set separated by a double white space)
#
# t678.n.bb2  map:0.1531 gm_map:0.0413 Rprec:0.1966 P_5:0.3640 P_10:0.3260

BEGIN {
     # TODO: consider using or dropping
     # getline root <"../config"

     L = 84  # number of systems, also the number of lines in each file
     M = 10  # number of test collections
     N = 5   # number of measures

     names = "t678 t678-fr t6 t7 t8 fbis fr94 ziff1 ziff2 ziff3"
     # names = "t678 t678-fr"
     # names = "t6 t7 t8" 
     # names = "fbis fr94"
     # names = "ziff1 ziff2 ziff3"

     # random index and names
     # rand_int  = "2 1"
     rand_int  = "3 9 2 6 5 4 10 7 1 8"
     rand_char = "A B C D E F G  H I J"
     split(rand_int, u, " ")

     # # not sure if needed, nevertheless
     # for (i=1; i <= M; i++)
     # 	  u[i] = int(u[i])

     split(rand_char, u_, " ")

     measures = "map gm_map Rprec P_5 P_10"

     # TODO: odd to check M, N this way, rather, use what split()
     # returns
     if(split(names, f, " ") != M) {
	  print "Error: number of test collections != M"
	  exit
     }

     if(split(measures, g, " ") != N) {
	  print "Error: number of measures != N"
	  exit
     }

     # prepare table headers

     # N floating point values each 6 chars long, with N - 1 spaces
     # between them, plus 2 white spaces separating test collection
     # blocks.

     w = N * 6 + (N - 1) + 2

     fmt = "%-20s"

     # format the test collection header

     h1 = sprintf(fmt, "")
     for (i=1; i <= M; i++)
     {
	  fmt_ = "%-*s"
	  # h1 = h1 sprintf(fmt_, w, f[i])
	  h1 = h1 sprintf(fmt_, w, u_[u[i]])
     }
     h1 = h1 sprintf("\n")

     # format a separator
     
     sep = ""
     for (i=0; i<w-2; i++)
	  sep = sep "-"

     h0 = sprintf(fmt, "")
     for (i=1; i <= M; i++)
     {
	  fmt_ = "%-*s"
	  h0 = h0 sprintf(fmt_, w, sep)
     }
     h0 = h0 sprintf("\n")
     
     # format the measures header

     h2 = sprintf(fmt, "")
     for (i=1; i <= M; i++)
     {
     	  for (j=1; j <= N; j++)
     	       h2 = h2 sprintf("%-6s ", g[j])
     	  h2 = h2 sprintf(" ")
     }
     h2 = h2 sprintf("\n")

     # write out neat headers
     # printf(h1)
     # printf(h0)
     # printf(h2)
     # printf(h0)
     
     for (i=1; i <= L; i++)
     {
	  s["dummy"] = ""
     	  for (j=1; j <= M; j++)
	  {
	       # rtag = f[j]
	       rtag = f[u[j]]
	       v = ""
	       f_ = "../../viz/" rtag ".measures"

     	       getline a[j] <f_

	       split(a[j], a_, " ")

	       # erase a part of the rtag
      
	       gsub(rtag ".", "", a_[1])

	       # clean up the values

	       for (k=2; k <= N+1; k++)
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

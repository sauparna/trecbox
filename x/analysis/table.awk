# Usage: awk -f table.awk [rand]
# Run the script from inside x/analysis/ directory. TODO: clean this up
# prints all 5 measures for all 84 systems for all 10 test collections
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
     M = 7   # number of test collections
     N = 5   # number of measures

     names = "t6 t7 t8 t678-fr fr94 ziff1 ziff2"
     M = split(names, f, " ")

     measures = "map gm_map Rprec P_5 P_10"
     N = split(measures, g, " ")

     # random index and names
     rand_int  = "1 2 3 4 5 6 7"
     split(rand_int, u, " ")

     # a knuth shuffle
     for (i=M; i>=2; i--)
     {
	  j = int(i * rand()) + 1
	  t = u[j]
	  u[j] = u[i]
	  u[i] = t
     }

     # make a note of the ordering
     rand_f = "../../viz/rand"
     for(i=1; i<=M; i++)
	  printf("%d ", u[i]) >rand_f
     printf("\n") >rand_f
     for(i=1; i<=M; i++)
	  printf("%s ", f[u[i]]) >rand_f
     printf("\n") >rand_f

     rand_char = "A B C D E F G"
     split(rand_char, u_, " ")

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
	       if (ARGV[1] ~ /rand/)
		    rtag = f[u[j]]
	       else
		    rtag = f[j]

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

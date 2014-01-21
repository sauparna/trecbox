# prettyprint the tab0.1
# they are usually named tab0.*.map, where 'map' is the measure

BEGIN{
     # f = "../../viz/tab0.1"
     f = "../../viz/tab0.1.rand"
     if (f ~ /rand/)
	  h = "A B C D E F G H I J"
	  # h = "t6 ziff2 t678-fr fbis t8 t7 ziff3 fr94 t678 ziff1"
     else
	  h = "t678 t678-fr t6 t7 t8 fbis fr94 ziff1 ziff2 ziff3"
     n = split(h, a, " ")
     h1 = sprintf("%-4s %-11s %-8s", "stem", "model", "measure")
     for (i=1; i<=n; i++)
	  h1 = h1 sprintf("%-8s", a[i])
     h1 = h1 sprintf("\n")
     
     printf(h1)

     c = 1
     s = ""
     while(getline <f)
     {
	  s = sprintf("%-4s %-11s %-8s", $1, $2, $3)
	  n = split($0, a, " ")
	  for (i=4; i<=n; i++)
	       s = s sprintf("%-8s", a[i])
	  printf("%s\n", s)
	  if (c % 5 == 0)
	       printf("\n")
	  c++
	  s = ""
     }
}

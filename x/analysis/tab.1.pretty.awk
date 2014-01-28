BEGIN{

     if (ARGC < 2)
     {
	  print "usage: awk -f tab.1.pretty.awk <file> [hide]"
	  print "e.g. awk -f tab.1.pretty.awk ../../viz/tab.1 hide"
	  print "e.g. awk -f tab.1.pretty.awk ../../viz/tab.1.rand hid"
	  print "e.g. awk -f tab.1.pretty.awk ../../viz/tab.1.rand.map hidden"
	  exit
     }

     f = ARGV[1]

     hide = 0
     if (ARGC > 2)
     {
	  if(ARGV[2] ~ /hid/)
	       hide = 1
     }

     if (f ~ /rand/)
     {
	  if (hide)
	       h = "A B C D E F G"
	  else
	       h = "t8 t678-fr ziff1 t6 fr94 ziff2 t7"
     }
     else
	  h = "t6 t7 t8 t678-fr fr94 ziff1 ziff2"

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

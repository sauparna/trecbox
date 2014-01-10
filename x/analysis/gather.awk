# gather the measures in one line
{
     if(NR%5==0) 
     {
	  s = s " " $2 ":" $3;
	  print $1 " " s;
	  s = ""
     }
     else 
	  s = s " " $2 ":" $3
}
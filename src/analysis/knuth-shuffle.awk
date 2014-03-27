function knuth_shuffle(a)
{
     n = 0
     for (i in a)
	  n++
     for (i=n-1; i>=1; i--)
     {
	  j = int((i+1) * rand())
	  t = a[j]
	  a[j] = a[i]
	  a[i] = t
     }
}

BEGIN {
     for(i=0; i<10; i++)
	  a[i] = i
     for (i in a)
	  n++
     for (i=0; i<n; i++)
	  printf("%d ", a[i])
     printf("\n")
     knuth_shuffle(a)
     for (i=0; i<n; i++)
	  printf("%d ", a[i])
     printf("\n")
}
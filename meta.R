library(metafor)
library(xtable)
meta_analysis = function(in_d, out_d)
{
  path    = list.files(path=in_d, full.names=T)
  n       = length(path)
  tab     = vector("list", n)
  es.D    = vector("list", n)
  es.R    = vector("list", n)
  ma.D.RE = vector("list", n)
  ma.R.RE = vector("list", n)
  for(i in 1:n) {
    # read in the tables, and normalise 0 scores to 0.0001
    # or else response ratio computations will produce +-Inf which
    # would get coded to NAs.

    tab[[i]]  = read.table(path[i], header=T)
    tab[[i]][tab[[i]] == 0.0] = 0.0001

    # calculate ES and write to file

    es.D[[i]] = escalc(data=tab[[i]], measure="MD",  m1i=m1,sd1i=s1,n1i=n1, m2i=m2,sd2i=s2,n2i=n2, append=T, var.names=c("y_", "v_"))
    es.R[[i]] = escalc(data=tab[[i]], measure="ROM", m1i=m1,sd1i=s1,n1i=n1, m2i=m2,sd2i=s2,n2i=n2, append=T, var.names=c("y_", "v_"))

    oname = paste(basename(path[i]), "D.RE", "tex", sep=".")
    ofile = paste(out_d, oname, sep="/")
    print(xtable(es.D[[i]], caption=basename(path[i]), digits=c(0,0,4,4,0,4,4,0,4,4,4,4,4,4,4,4)), type="latex", file=ofile)

    oname = paste(basename(path[i]), "R.RE", "tex", sep=".")
    ofile = paste(out_d, oname, sep="/")
    print(xtable(es.R[[i]], caption=basename(path[i]), digits=c(0,0,4,4,0,4,4,0,4,4,4,4,4,4,4,4)), type="latex", file=ofile)

    # Do the meta-analysis and write summary and plot to file

    ma.D.RE[[i]] = rma.uni(data=es.D[[i]], y_, v_, method="DL")
    ma.R.RE[[i]] = rma.uni(data=es.R[[i]], y_, v_, method="DL")

    # summary
    oname = paste(basename(path[i]), "D.RE", "summary", sep=".")
    ofile = paste(out_d, oname, sep="/")
    sink(file=ofile)
    print(summary(ma.D.RE[[i]]))
    sink(NULL)
    
    oname = paste(basename(path[i]), "R.RE", "summary", sep=".")
    ofile = paste(out_d, oname, sep="/")
    sink(file=ofile)
    print(summary(ma.R.RE[[i]]))
    sink(NULL)

    # plots
    oname = paste(basename(path[i]), "D.RE", "pdf", sep=".")
    ofile = paste(out_d, oname, sep="/")
    pdf(ofile)
    print(forest.rma(ma.D.RE[[i]], digit=c(2, 2), slab=es.R[[i]]$testcol, xlim=c(8, -6), alim=c(-3.5,3.5)))
    #print(forest.rma(ma.D.RE[[i]], digit=c(2, 2), slab=es.R[[i]]$testcol))
    dev.off()
    
    oname = paste(basename(path[i]), "R.RE", "pdf", sep=".")
    ofile = paste(out_d, oname, sep="/")
    pdf(ofile)
    print(forest.rma(ma.R.RE[[i]], digit=c(2, 2), slab=es.R[[i]]$testcol, xlim=c(8, -6), alim=c(-3.5,3.5)))
    #print(forest.rma(ma.R.RE[[i]], digit=c(2, 2), slab=es.R[[i]]$testcol))
    dev.off()
  }
}

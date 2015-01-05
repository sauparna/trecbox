library(metafor)
library(xtable)
library(gridExtra)
library(gdata)

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

    es.D[[i]] = escalc(data=tab[[i]], measure="MD",  m1i=m2,sd1i=s2,n1i=n2, m2i=m1,sd2i=s1,n2i=n1, append=T, var.names=c("y_", "v_"))
    es.R[[i]] = escalc(data=tab[[i]], measure="ROM", m1i=m2,sd1i=s2,n1i=n2, m2i=m1,sd2i=s1,n2i=n1, append=T, var.names=c("y_", "v_"))

    ## TODO: table columns have increased.
    
    ## ## oname = paste(basename(path[i]), "D.RE", "tex", sep=".")
    ## oname = paste(basename(path[i]), "D.RE", "tab", "pdf", sep=".")
    ## ofile = paste(out_d, oname, sep="/")
    ## ## print(xtable(es.D[[i]], caption=basename(path[i]), digits=c(0,0,4,4,0,4,4,0,4,4,4,4,4,4,4,4)), type="latex", file=ofile)
    ## pdf(ofile, height=11, width=8.5)
    ## print(grid.table(es.D[[i]]))
    ## dev.off()

    ## ## oname = paste(basename(path[i]), "R.RE", "tex", sep=".")
    ## oname = paste(basename(path[i]), "R.RE", "tab", "pdf", sep=".")
    ## ofile = paste(out_d, oname, sep="/")
    ## ## print(xtable(es.R[[i]], caption=basename(path[i]), digits=c(0,0,4,4,0,4,4,0,4,4,4,4,4,4,4,4)), type="latex", file=ofile)
    ## pdf(ofile, height=11, width=8.5)
    ## print(grid.table(es.R[[i]], gp=gpar(fontsize=7)))
    ## dev.off()

    oname = paste(basename(path[i]), "R.RE", "txt", sep=".")
    ofile = paste(out_d, oname, sep="/")
    write.fwf(es.R[[i]], file=ofile, sep=" ", quote=F, rownames=T)
    
    # Do the meta-analysis and write summary and plot to file

    # NOTE: metafor's v_ differs from v
    ma.D.RE[[i]] = rma.uni(data=es.D[[i]], yi=y, vi=v, tau2=tab[[i]]$tau2, method="DL")
    ma.R.RE[[i]] = rma.uni(data=es.R[[i]], yi=y, vi=v, tau2=tab[[i]]$tau2, method="DL")
    ## ma.D.RE[[i]] = rma.uni(data=es.D[[i]], yi=y_, vi=v_, tau2=tab[[i]]$tau2, method="DL")
    ## ma.R.RE[[i]] = rma.uni(data=es.R[[i]], yi=y_, vi=v_, tau2=tab[[i]]$tau2, method="DL")

    # summary
    oname = paste(basename(path[i]), "D.RE", "s", sep=".")
    ofile = paste(out_d, oname, sep="/")
    sink(file=ofile)
    print(summary(ma.D.RE[[i]]))
    sink(NULL)
    
    oname = paste(basename(path[i]), "R.RE", "s", sep=".")
    ofile = paste(out_d, oname, sep="/")
    sink(file=ofile)
    print(summary(ma.R.RE[[i]]))
    sink(NULL)

    # plots
    oname = paste(basename(path[i]), "D.RE", "pdf", sep=".")
    ofile = paste(out_d, oname, sep="/")
    pdf(ofile)
    print(forest.rma(ma.D.RE[[i]], digit=c(2, 2), refline=0, slab=es.R[[i]]$testcol, mlab="m2-m1, RE", xlab=basename(path[i])))
    #print(forest.rma(ma.D.RE[[i]], digit=c(2, 2), slab=es.R[[i]]$testcol))
    dev.off()
    
    oname = paste(basename(path[i]), "R.RE", "pdf", sep=".")
    ofile = paste(out_d, oname, sep="/")
    pdf(ofile)
    print(forest.rma(ma.R.RE[[i]], digit=c(2, 2),  refline=0, slab=es.R[[i]]$testcol, mlab="log(m2/m1), RE", xlab=basename(path[i])))
    #print(forest.rma(ma.R.RE[[i]], digit=c(2, 2), slab=es.R[[i]]$testcol))
    dev.off()
  }
}

# Given a directory of tables, it outputs bar plots of relevance
# counts in another output directory. The third arg MAX is the maximum
# x-axis value of the plots.

library(xtable)

qrelsplot = function(in_d, out_d, MAX)
{
    name = list.files(path=in_d)
    path = list.files(path=in_d, full.names=T)
    n = length(name)
    tab = vector("list", n)
    mlt = vector("list", n)
    plt = vector("list", n)
    for(i in 1:n){
        tab[[i]] = read.table(path[i], header=T)

        oname = paste(basename(path[i]), "r", "plot", "pdf", sep=".")
        ofile = paste(out_d, oname, sep="/")
        pdf(ofile)
        print(barplot(tab[[i]]$r, ylim=c(0,MAX), names.arg=tab[[i]]$id, xlab="Topic ID", ylab="# relevant docs"))
        dev.off()

        oname = paste(basename(path[i]), "r", "tex", sep=".")
        ofile = paste(out_d, oname, sep="/")
        print(xtable(tab[[i]], caption=basename(path[i])), type="latex", file=ofile)
    }
}

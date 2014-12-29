# Given a directory of tables, it outputs bar plots of relevance
# counts in another output directory. The third arg YMAX is the maximum
# y-axis value of the plots.

library(xtable)

qrelsplot = function(in_d, out_d, YMAX, sort=0)
{
    name = list.files(path=in_d)
    path = list.files(path=in_d, full.names=T)
    n = length(name)
    tab = vector("list", n)

    for(i in 1:n){
        tab[[i]] = read.table(path[i], header=T)
        if(sort == 1){
            tab[[i]] = tab[[i]][order(tab[[i]]$total),]
        }
        ## row.names(tab[[i]]) = 1:nrow(tab[[i]])
        oname = paste(basename(path[i]), "R", "plot", "pdf", sep=".")
        ofile = paste(out_d, oname, sep="/")

        pdf(ofile)
        print(barplot(tab[[i]]$total, ylim=c(0,YMAX), names.arg=tab[[i]]$QID, xlab="Topic ID", ylab="# relevant", las=2, cex.names=0.5))
        dev.off()
        oname = paste(basename(path[i]), "R", "tex", sep=".")
        ofile = paste(out_d, oname, sep="/")
        print(xtable(tab[[i]], caption=basename(path[i])), type="latex", file=ofile)
    }
}

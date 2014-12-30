# Given a directory of tables, it outputs bar plots of relevance
# counts in another output directory. The third arg YMAX is the maximum
# y-axis value of the plots.

library(xtable)
library(ggplot2)

qrelsplot = function(in_d, out_d, YMAX, sort=0)
{
    name = list.files(path=in_d)
    path = list.files(path=in_d, full.names=T)
    n    = length(name)
    tab  = vector("list", n)
    txt  = c("<= 5", "<= 10", "<= 50", "<= 100", "> 100")
    cbPalette = c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

    for(i in 1:n){
        tab[[i]] = read.table(path[i], header=T)
        if(sort == 1){
            tab[[i]] = tab[[i]][order(tab[[i]]$total),]
        }
        ## row.names(tab[[i]]) = 1:nrow(tab[[i]])
        oname = paste(basename(path[i]), "R", "plot", "pdf", sep=".")
        ofile = paste(out_d, oname, sep="/")
        df = tab[[i]]

        #bp = barplot(tab[[i]]$total, ylim=c(0,YMAX), names.arg=tab[[i]]$QID, xlab="Topic ID", ylab="# relevant", las=2, cex.names=0.5)
        bp = ggplot(df, aes(x=reorder(factor(QID), total), y=total, fill=factor(bin))) + geom_bar(stat="identity")
        ## bp = bp + scale_fill_discrete(breaks=levels(factor(df$bin)), labels=txt)
        bp = bp + scale_fill_manual(values=cbPalette, breaks=levels(factor(tab$bin)), labels=txt)
        bp = bp + theme(axis.text.x=element_text(angle=90, vjust=0.5, size=2))
        bp = bp + scale_fill_hue(c=45, l=80)

        pdf(ofile)
        print(bp)
        dev.off()

        xt = xtable(tab[[i]], caption=basename(path[i])), type="latex", file=ofile
        
        oname = paste(basename(path[i]), "R", "tex", sep=".")
        ofile = paste(out_d, oname, sep="/")
        print(xt)
    }
}

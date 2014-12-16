library(ggplot2)
plotforest = function(tab)
{
    ggplot(data=tab, aes(x=y, y=testcol)) +
        geom_point(aes(size=W, fill=testcol), colour="black", shape=22) +
        geom_errorbarh(aes(xmin=l, xmax=u), height=0.0) +
        geom_vline(xintercept=0, linetype="dashed") +
        geom_text(aes(x=2.8, label=testcol), size=4)
}

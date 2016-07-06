

library(dplyr)
library(ggplot2)

setwd(paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/res-netlogo'))

res <- as.tbl(read.csv('20160705_grid/2016_07_05_01_14_59_grid.csv'))

sres = res %>% group_by(id) %>% summarise(
  diversityTrend=mean(diversityTrend),intellibility=mean(intellibility),languageDiversity=mean(languageDiversity),
  languageSize=mean(languageSize),initVariability=mean(initVariability),mutationRate=mean(mutationRate),populationSize=mean(populationSize),
  semanticSize=mean(semanticSize),understandingThreshold=mean(understandingThreshold)
 )

indics = c("diversityTrend","intellibility","languageDiversity","languageSize")

plotlist = list()
for(indic in indics){
  g = ggplot(sres,aes_string(x="mutationRate",y="understandingThreshold",fill=indic))
  plotlist[[indic]]=g+geom_raster(hjust=0,vjust=0)+facet_grid(populationSize~semanticSize+initVariability,scales = "free")+scale_fill_gradient(low='yellow',high='red')
}
multiplot(plotlist=plotlist,cols=2)




library(dplyr)
library(ggplot2)

setwd(paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/src-netlogo'))

#res <- as.tbl(read.csv('20160706_gridrefined/2016_07_06_23_16_09_grid_refined_all.csv'))
res <- as.tbl(read.csv('res/exploration/2017_01_04_10_37_51_memory_local.csv'))

sres = res %>% group_by(id) %>% summarise(
  diversityTrendSd=sd(diversityTrend),diversityTrend=mean(diversityTrend),
  intelligibilitySd=sd(intelligibility),intelligibility=mean(intelligibility),
  languageDiversitySd=sd(languageDiversity),languageDiversity=mean(languageDiversity),
  languageSizeSd=sd(languageSize),languageSize=mean(languageSize),
  initVariability=mean(initVariability),mutationRate=mean(mutationRate),populationSize=mean(populationSize),
  semanticSize=mean(semanticSize),understandingThreshold=mean(understandingThreshold),
  memoryImpedance=mean(memoryImpedance)
 )

indics = c("diversityTrend","intellibility","languageDiversity","languageSize")

plotlist = list()
for(indic in indics){
  g = ggplot(sres,aes_string(x="mutationRate",y="understandingThreshold",fill=indic))
  plotlist[[indic]]=g+geom_raster(hjust=0,vjust=0)+facet_wrap(~initVariability,scales = "free")+scale_fill_gradient(low='yellow',high='red')
}
multiplot(plotlist=plotlist,cols=2)


##
g=ggplot(sres,aes(x=memoryImpedance,y=languageSize,colour=understandingThreshold,group=understandingThreshold))
g+geom_point()+geom_line()#+geom_errorbar(aes(ymin=languageDiversity-languageDiversitySd,ymax=languageDiversity+languageDiversitySd))


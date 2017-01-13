

library(dplyr)
library(ggplot2)
source(paste0(Sys.getenv("CN_HOME"),'/Models/Utils/R/plots.r'))

setwd(paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/src-netlogo'))
resdirprefix = paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/res-netlogo/')

res <- as.tbl(read.csv('../res-netlogo/20160706_gridrefined/2016_07_06_23_16_09_grid_refined_all.csv'))
#res <- as.tbl(read.csv('res/exploration/2017_01_04_10_37_51_memory_local.csv'))
#res <- as.tbl(read.csv('res/exploration/2017_01_12_15_06_09_memory_local.csv'))


sres = res %>% group_by(mutationRate,understandingThreshold) %>% summarise(
  diversityTrendSd=sd(diversityTrend),diversityTrend=mean(diversityTrend),
  intelligibilitySd=sd(intellibility),intelligibility=mean(intellibility),
  languageDiversitySd=sd(languageDiversity),languageDiversity=mean(languageDiversity)/100,
  languageSizeSd=sd(languageSize),languageSize=mean(languageSize),
  initVariability=mean(initVariability),populationSize=mean(populationSize),
  count=n()
)

res$id2 = as.character(res$understandingThreshold*10000 + res$mutationRate*100)

sres = res %>% group_by(id) %>% summarise(
  diversityTrendSd=sd(diversityTrend),diversityTrend=mean(diversityTrend),
  intelligibilitySd=sd(intelligibility),intelligibility=mean(intelligibility),
  languageDiversitySd=sd(languageDiversity),languageDiversity=mean(languageDiversity),
  languageSizeSd=sd(languageSize),languageSize=mean(languageSize),
  initVariability=mean(initVariability),mutationRate=mean(mutationRate),populationSize=mean(populationSize),
  semanticSize=mean(semanticSize),understandingThreshold=mean(understandingThreshold),
  memoryImpedance=mean(memoryImpedance),wanderingRadius=mean(wanderingRadius),
  medDiversity=quantile(smoothedDiversity,0.5)/100,smoothedDiversitySd=sd(smoothedDiversity)/100,smoothedDiversity=mean(smoothedDiversity)/100,
  medIntelligibility=quantile(smoothedIntelligibility,0.5),smoothedIntelligibilitySd=sd(smoothedIntelligibility),smoothedIntelligibility=mean(smoothedIntelligibility)
)



#####
## Exploration

# heatmaps

indics = c("intelligibility","languageDiversity")#,"languageSize","diversityTrend")
legnames = c(expression(C(t[f])),expression(D(t[f])))#,'size','trend')

plotlist = list()
for(i in 1:length(indics)){
  g = ggplot(sres,aes_string(x="mutationRate",y="understandingThreshold",fill=indics[i]))
  plotlist[[i]]=g+geom_raster(hjust=0,vjust=0)+scale_fill_gradient(low='yellow',high='red',name=legnames[i])+
    xlab(expression(mu))+ylab(expression(theta))
}
multiplot(plotlist=plotlist,cols=1)



###
# histograms
res$id2 = as.character(res$id)
param_points = c("3","13","23")
sample = res[res$id2%in%param_points,]

plotlist = list()
for(indic in  c("intellibility","languageDiversity")){
  g=ggplot(sample)
  plotlist[[indic]]=g+geom_density(aes_string(x=indic,fill="id2",group="id2"),alpha=0.4)
}
multiplot(plotlist=plotlist,cols=1)


####
#  Memory effect

resdir = paste0(resdirprefix,'20170112_memory');dir.create(resdir)

# inteligibility = f(memory impedance)
g=ggplot(sres,aes(x=memoryImpedance,y=smoothedIntelligibility,colour=understandingThreshold,group=understandingThreshold))
g+geom_point()+geom_line()+geom_errorbar(aes(ymin=smoothedIntelligibility-smoothedIntelligibilitySd,ymax=smoothedIntelligibility+smoothedIntelligibilitySd))+
  xlab(expression(alpha[x]))+ylab("C")+scale_colour_continuous(name=expression(theta))+ theme(axis.title = element_text(size = 22),legend.title = element_text(size = 22), axis.text.x = element_text(size = 15),   axis.text.y = element_text(size = 15))
ggsave(file=paste0(resdir,'/memory-intelig.pdf'),width=10,height=7)

# diversity = f(memory impedance)
g=ggplot(sres,aes(x=memoryImpedance,y=smoothedDiversity,colour=understandingThreshold,group=understandingThreshold))
g+geom_point()+geom_line()+geom_errorbar(aes(ymin=smoothedDiversity-smoothedDiversitySd,ymax=smoothedDiversity+smoothedDiversitySd))+
  xlab(expression(alpha[x]))+ylab("D")+scale_colour_continuous(name=expression(theta))+ theme(axis.title = element_text(size = 22),legend.title = element_text(size = 22), axis.text.x = element_text(size = 15),   axis.text.y = element_text(size = 15))
ggsave(file=paste0(resdir,'/memory-diversity.pdf'),width=10,height=7)




##
g=ggplot(sres,aes(x=wanderingRadius,y=medIntelligibility,colour=understandingThreshold,group=understandingThreshold))
g+geom_point()+geom_line()#+geom_errorbar(aes(ymin=smoothedIntelligibility-smoothedIntelligibilitySd,ymax=smoothedIntelligibility+smoothedIntelligibilitySd))


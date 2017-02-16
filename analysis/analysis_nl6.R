
library(dplyr)
library(ggplot2)

setwd(paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/src-netlogo6'))

res <- as.tbl(read.csv('res/language_NL6 grid_mu_theta-table.csv',skip = 6))

g=ggplot(data.frame(modularity=res$max.network.modularity,theta=res$understanding.threshold,mu=res$X..random.mutations),aes(x=mu,y=modularity,colour=theta,group=theta))
g+geom_point()+geom_line()


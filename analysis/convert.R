
library(igraph)

setwd(paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/src-netlogo6'))

#dir = 'theta0.3_mu0.1_seed-85791'
dir='theta0.1_mu0.3_seed34869'

for(time in seq(from=1001,to=5001,by=1000)){
  #time='10000'
  
  #edf = read.csv(paste0('res/networks/',dir,'/',time,'.csv'),sep=' ',header=TRUE)
  edf = read.csv(paste0('res/networks/',dir,'_',time,'.csv'),sep=' ',header=TRUE)
  
  
  g = graph_from_data_frame(edf,directed=FALSE)
  E(g)$weight = 1/(E(g)$distance^2)
  #cluster_louvain(g)
  
  write_graph(g,paste0('res/networks/',dir,'_',time,'.gml'),format = 'gml')
}




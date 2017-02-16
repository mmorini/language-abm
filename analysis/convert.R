
library(igraph)

setwd(paste0(Sys.getenv('CS_HOME'),'/LanguageEvolution/language-abm/src-netlogo'))

dir = 'theta0.3_mu0.1_seed-85791'
time='20000'

edf = read.csv(paste0('res/networks/',dir,'/',time,'.csv'),sep=' ',header=TRUE)

g = graph_from_data_frame(edf,directed=FALSE)

write_graph(g,paste0('res/networks/',dir,'/',time,'.gml'),format = 'gml')

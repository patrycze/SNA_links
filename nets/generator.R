library(igraph)
library(plyr)
setwd("C:/Users/Patryk/Desktop/SNA_links/nets")

for (neix in seq(1,3, by=1 )){
  
  for (i in seq(0, 1, by=0.25)){
    output = paste("ws_",neix,"_",i, sep = "")
    outputfile=paste(output, ".txt", sep = "")
    g5 <- watts.strogatz.game(dim=1, size=200, nei=neix, p= i )
    write.graph(graph = g5, file = outputfile  , format = "edgelist")
    weights(output)
    measures(output)
  }
  
}




for (i in seq(1, 1.2, by=0.1)){
  
  output=paste("ba1_",i, sep = "")
  outputfile=paste(output, ".txt", sep = "")
  g5 <- barabasi.game(16, m = i, directed = FALSE)
  write.graph(graph = g5, file = outputfile  , format = "edgelist")
  weights(output)
#  measures(output)
  
  print(i)
  
}




for (m in seq(200, 1000, by=200)){
  
  
  output=paste("er_",m, sep = "")
  outputfile=paste(output, ".txt", sep = "")
  g5 <- erdos.renyi.game(200, m  , type=c("gnm"), directed = FALSE)
  write.graph(graph = g5, file = outputfile  , format = "edgelist")
  weights(output)
  measures(output)
  
  
}



















weights <- function(net){
  
  for (idx in 1:1000) {
    netx = paste(net,".txt",sep = "")
    dat1 <- read.csv(netx,header=FALSE,sep=" ")
    colnames(dat1)[1] <- "a"
    colnames(dat1)[2] <- "b"
    dat1$rnd1 <- sample(100, size = nrow(dat1), replace = TRUE)
    dat1$rnd2 <- sample(100, size = nrow(dat1), replace = TRUE)
    dat1$rnd1 <- dat1$rnd1/100
    dat1$rnd2 <- dat1$rnd2/100
    write.table(dat1, paste("networks/",net,"_",idx,".txt",sep=""), sep=" ", row.names=FALSE, col.names=FALSE) 
  }
  
  
}






measures <- function(net){
  
  g1 <- read.graph(paste(net,".txt",sep=""), format="edgelist")
  numofnodes = vcount(g1) 
  numofedges = ecount(g1) 
  
  measure1 <- degree(g1)
  m2 <- evcent(g1, directed = FALSE,weights = NULL)
  measure2 <- data.frame(m2[1])
  measure3 <- betweenness(g1, v=V(g1), directed = FALSE, weights = NULL,  nobigint = TRUE, normalized = FALSE)
  
  nodeid<-measure1
  
  for(j in 1:numofnodes) 
  {   
    nodeid[ j ] = j - 1
  }
  
  write.csv(measure1,    file = paste("measures/",net,"_dg.txt",sep=""),row.names=FALSE)
  write.csv(measure2,    file = paste("measures/",net,"_ev.txt",sep=""),row.names=FALSE)
  write.csv(measure3,    file = paste("measures/",net,"_bt.txt",sep=""),row.names=FALSE)
  
  
  
  
  measure4<- neighborhood.size(g1, 2, nodes=V(g1))
  measure5<-closeness(g1,normalized = TRUE,mode="all")
  measure6<-page_rank(g1)
  
  
  write.csv(measure4,    file = paste("measures/",net,"_dg2.txt",sep=""),row.names=FALSE)
  write.csv(measure5,    file = paste("measures/",net,"_cl.txt",sep=""),row.names=FALSE)
  write.csv(measure6[1], file = paste("measures/",net,"_pr.txt",sep=""),row.names=FALSE)
  
  file = paste("measures/",net,"_dg.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z <- z[order(z$x, decreasing =    TRUE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  write.table(z, file = paste("rankings/",net,"_ranking_dg.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  file = paste("measures/",net,"_dg.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z$rnd <- sample(10000, size = nrow(z), replace = TRUE)
  z$rnd <- z$rnd/100
  z <- z[order(z$rnd, decreasing    = FALSE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  z  <- subset(z, select = c(node, rnd,rank))
  write.table(z, file = paste("rankings/",net,"_ranking_rn.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  file = paste("measures/",net,"_dg2.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z <- z[order(z$x, decreasing    = TRUE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  write.table(z, file = paste("rankings/",net,"_ranking_dg2.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  file = paste("measures/",net,"_cl.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z <- z[order(z$x, decreasing = FALSE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  write.table(z, file = paste("rankings/",net,"_ranking_cl.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  file = paste("measures/",net,"_ev.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z <- z[order(z$vector, decreasing    = TRUE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  write.table(z, file = paste("rankings/",net,"_ranking_ev.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  file = paste("measures/",net,"_pr.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z <- z[order(z$vector, decreasing    = TRUE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  write.table(z, file = paste("rankings/",net,"_ranking_pr.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  file = paste("measures/",net,"_bt.txt",sep="");
  fx = read.csv(file, header = TRUE, sep = "")
  nr = nrow(fx)
  nr = nr - 1 
  node <- rep(0:nr)
  z <- cbind(node,fx)
  z <- z[order(z$x, decreasing    = TRUE),]
  nr = nr + 1 
  rank <- rep(1:nr)
  z <- cbind(z,rank)
  write.table(z, file = paste("rankings/",net,"_ranking_bt.txt",sep=""),row.names=FALSE,col.names=FALSE,sep=" ")
  
  print("88");
  
}

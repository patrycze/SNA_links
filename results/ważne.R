

setwd("/Users/apple/Desktop/SNA_links/results")


data = read.csv('resultWithE.csv', header=FALSE,sep=",")


data$meanInfections <- ave(data$coverage, data$net, data$len, FUN=mean) # okreslenie średniej wartości i przypisanie ich do tabeli

data$diff <- ave(data$V2, FUN=function(x) c(0, diff(x)))

data$len <- nchar(as.character(data$seed))

data1 <- subset(data, select = c(V2,V5,V6,V7,V8))


net4 <- as.data.frame(data[grep("^4", data$net),])
net5 <- as.data.frame(data[grep("^5", data$net),])
net6 <- as.data.frame(data[grep("^6", data$net),])

net4$meanCov <- ave(net4$coverage, net4$len, FUN=mean)
net5$meanCov <- ave(net5$coverage, net5$len, FUN=mean)
net6$meanCov <- ave(net6$coverage, net6$len, FUN=mean)

net4 <- subset(net4, select = c(seed, meanCov))
net5 <- subset(net5, select = c(seed, meanCov))
net6 <- subset(net6, select = c(seed, meanCov))

net4 <- as.data.frame(unique(net4[,2]))
net5 <- as.data.frame(unique(net5[,2]))
net6 <- as.data.frame(unique(net6[,2]))

net4 <- as.data.frame(net4[order(net4),])
net5 <- as.data.frame(net5[order(net5),])
net6 <- as.data.frame(net6[order(net6),])


length <- rep(1:(length(net4[,1]) + length(net5[,1]) + length(net6[,1])))

length1 <- rep(1:(length(net4[,1])))
length2 <- rep(1:(length(net5[,1])))
length3 <- rep(1:(length(net6[,1])))

line1 <- t(net4)
line2 <- t(net5)
line3 <- t(net6)

png(paste("points.png"),width = 3000, height = 3000, res=300)

#plot(line3,length3,col="white",xlab="",  ylab="", cex.lab=2.5,mgp = c(2.5, 1, 0), cex.axis=2,log="xy" )
plot(data$V6,data$V2,col="white",xlab="",  ylab="", cex.lab=2.5,mgp = c(2.5, 1, 0), cex.axis=2,log="xy" )

title(ylab="coverage",mgp=c(2.5,1,0), cex.lab=2.5)
title(xlab="seed set",mgp=c(2.5,1,0), cex.lab=2.5)

points(data$V5,data$V2,col="red",  pch=20,  cex=0.4, bg="red") 
#lines(length1,line1,col="red",  pch=20,  cex=0.4, bg="yellow1") 
#lines(length2,line2,col="orange2",  pch=20,  cex=0.4, bg="yellow1") 
#lines(length3,line3,col="green2",  pch=20,  cex=0.4, bg="yellow1") 

colors <- c("red","orange2","green2", "blue", "yellow1")

legend("topleft", c("4 nodes","5 nodes","6 nodes"), col=colors, cex=2, lty=c(1,1), lwd=c(2,2), bty="n");

dev.off()


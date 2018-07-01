setwd("/Users/apple/Desktop/_infa/modelowanie\ dyfuzji/python/sym1/2/syntetic/RESULTS")

data = read.csv('ba1.5result.csv', header=TRUE,sep=",")

data$numberOfRanking <- as.numeric(data$pp) # tutaj określam po czym chce uśredniać np. po PP albo po rankingu
average = subset(data, pair == 'none')
average$meanInfections <- ave(as.numeric(as.character(average$infections)), as.numeric(average$sp), as.numeric(average$pp), as.numeric(average$greedy), FUN=mean) # okreslenie średniej wartości i przypisanie ich do tabeli

uniqueArevage <- subset(average, select = c(numberOfRanking, greedy, meanInfections))
uniqueArevage <- unique(uniqueArevage[, 3:1])

n <- as.numeric(unique(uniqueArevage[, 3]))
nRanking <- as.numeric(unique(uniqueArevage[, 3]))

xrange <- range(1:(length(uniqueArevage$meanInfections)/length(nRanking))) # zaklres dla osi X
yrange <- range(uniqueArevage$meanInfections) # zakres dla osi Y

png('test',width = 3000, height = 3000, res=300)
plot(xrange, yrange, main = '', type="n", xlab="number of links ", ylab="infections" )
title(main = "")
colors <- c("cornsilk4", "red","green2","orange2","blue", "salmon")
axisX = length(uniqueArevage$meanInfections)/length(nRanking)
linetype <- c(1:nRanking)
j = 0

for (i in nRanking) {
j = j+1
print(i)
chartSubset <- subset(uniqueArevage, numberOfRanking==i) 
axisX = length(chartSubset$meanInfections)
lines(1:axisX, chartSubset$meanInfections, col=colors[j], pch=21, cex=0.1, bg="green") 
}

legend("topleft", c("0.1", "0.2", "0.3", "0.4", "0.5") , col=colors, cex=1.5, lty=c(1,1), lwd=c(2,2), bty="n");
par(mar=c(5,5,2,2))
dev.off()


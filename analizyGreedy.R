# średnia liczba infekcji w stepie 

setwd("/Users/apple/Desktop/_infa/modelowanie\ dyfuzji/python/sym1/2/syntetic/RESULTS")

data = read.csv('ba1.5result.csv', header=FALSE,sep=",")
check = subset(data, V20 == '[]')
check = subset(data, V20 == '[[\'2\', \'15\']]')
check = subset(data, V20 == '[[\'2\', \'15\'], [\'7\', \'11\'], [\'6\', \'12\'], [\'0\', \'11\'], [\'7\', \'12\']]')
data$numberOfRanking <- as.numeric(data$V1) # przypisanie wartości liczbowej do metody
nRanking <- max(data$numberOfRanking)

dataWITH = subset(data, V19 == 'True')
dataWITHOUT = subset(data, V19 == 'False' )

dataWITH$meanInfections <- ave(dataWITH$V7, dataWITH$numberOfRanking, dataWITH$V5, FUN=mean) # okreslenie średniej wartości i przypisanie ich do tabeli
dataWITHOUT$meanInfections <- ave(dataWITHOUT$V7, dataWITHOUT$numberOfRanking, dataWITHOUT$V5, FUN=mean) # okreslenie średniej wartości i przypisanie ich do tabeli


avarageInfectionsWITH <- subset(dataWITH, select = c(numberOfRanking, V5, meanInfections)) # unikalne wartości średniego pokrycia dla kroku 
avarageInfectionsWITHOUT <- subset(dataWITHOUT, select = c(numberOfRanking, V5, meanInfections)) # unikalne wartości średniego pokrycia dla kroku 

tableWITH <- unique(avarageInfectionsWITH[, 3:1]) # unikalne wartości średniego pokrycia dla kroku 
tableWITHOUT <- unique(avarageInfectionsWITHOUT[, 3:1]) # unikalne wartości średniego pokrycia dla kroku 

tableWITH$ratio <- tableWITH$meanInfections/tableWITHOUT$meanInfections # okreslenie średniej wartości i przypisanie ich do tabeli
tableWITHOUT$ratio <- tableWITHOUT$meanInfections/tableWITH$meanInfections

valWITH = subset(tableWITH, ratio > 1)
valWITH = length(valWITH$ratio)/length(tableWITHOUT$ratio)


## BIGGEST DIFFERENCE

tableWITH$biggestDifference = tableWITH$meanInfections-tableWITHOUT$meanInfections
biggestDifference <- tableWITH[which.max(tableWITH$biggestDifference),]

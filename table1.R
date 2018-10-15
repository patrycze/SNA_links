setwd("/Users/apple/Desktop/SNA_links/greedy-OP/")

random = read.csv('test.csv', header=FALSE,sep=",")


random = read.csv('random-new.csv', header=FALSE,sep=",")
greedy = read.csv('greedy.csv', header=FALSE,sep=",")
max = read.csv('max.csv', header=FALSE,sep=",")

result = random

colnames(random)[1] = 'number'
colnames(random)[2] = 'net'
colnames(random)[3] = 'space'
colnames(random)[4] = 'R1'
colnames(random)[5] = 'R2'
colnames(random)[6] = 'R3'
colnames(random)[7] = 'R4'
colnames(random)[8] = 'R5'
colnames(random)[9] = 'R6'
colnames(random)[10] = 'R7'
colnames(random)[11] = 'R8'
colnames(random)[12] = 'R9'
colnames(random)[13] = 'R10'
colnames(random)[14] = 'R11'

colnames(greedy)[1] = 'number'
colnames(greedy)[2] = 'net'
colnames(greedy)[3] = 'space'
colnames(greedy)[5] = '1'
colnames(greedy)[6] = '2'
colnames(greedy)[7] = '3'
colnames(greedy)[8] = '4'
colnames(greedy)[9] = '5'
colnames(greedy)[10] = '6'
colnames(greedy)[11] = '7'
colnames(greedy)[12] = '8'
colnames(greedy)[13] = '9'
colnames(greedy)[14] = '10'
colnames(greedy)[15] = '11'
colnames(greedy)[16] = '12'

colnames(max)[1] = 'number'
colnames(max)[2] = 'net'
colnames(max)[3] = 'space'
colnames(max)[5] = '1'
colnames(max)[6] = '2'
colnames(max)[7] = '3'
colnames(max)[8] = '4'
colnames(max)[9] = '5'
colnames(max)[10] = '6'
colnames(max)[11] = '7'
colnames(max)[12] = '8'
colnames(max)[13] = '9'
colnames(max)[14] = '10'
colnames(max)[15] = '11'
colnames(max)[16] = '12'
colnames(max)[17] = '13'

random$G1 <- greedy[,'1']
random$G2 <- greedy[,'2']
random$G3 <- greedy[,'3']
random$G4 <- greedy[,'4']
random$G5 <- greedy[,'5']
random$G6 <- greedy[,'6']
random$G7 <- greedy[,'7']
random$G8 <- greedy[,'8']
random$G9 <- greedy[,'9']
random$G10 <- greedy[,'10']
random$G11 <-  greedy[,'11']
random$G12 <-  greedy[,'12']
random$G13 <- 0

random$R12 <- 0
random$R13 <- 0



random$M1 <- max[,'1']
random$M2 <- max[,'2']
random$M3 <- max[,'3']
random$M4 <- max[,'4']
random$M5 <- max[,'5']
random$M6 <- max[,'6']
random$M7 <- max[,'7']
random$M8 <- max[,'8']
random$M9 <- max[,'9']
random$M10 <- max[,'10']
random$M11 <- max[,'11']
random$M12 <- max[,'12']
random$M13 <- max[,'13']


result = subset(random, select = c('number','net', 'space', 'R1', 'G1', 'M1', 'R2', 'G2', 'M2', 'R3', 'G3', 'M3', 'R4', 'G4', 'M4', 'R5', 'G5', 'M5', 'R6', 'G6', 'M6'
                                   , 'R7', 'G7', 'M7', 'R8', 'G8', 'M8', 'R9', 'G9', 'M9', 'R10', 'G10', 'M10', 'R11', 'G11', 'M11', 'R12', 'G12', 'M12', 'R13', 'G13', 'M13'))


new_df$meanCoverage <- ave(new_df$coverage, new_df$net, FUN=mean)

test <- unique(new_df[,c(4,5,6,7,8,9,10,11,12)])

test <- merge(random, greedy)


colnames(dataE)[1] = 'net'

result = merge(test, dataE, by=c("net"))

result = subset(result, select = c('net', 'meanCoverage', 'V3','V4', 'V5', 'V6','V7','V8'))

write.csv(result, file = "resultWithE-REPAIR.csv",row.names=FALSE)


from igraph import *
import random
#import matplotlib.pyplot as plt
#import numpy as np
#load data into a graph
import csv
import time

def readFileToArray(file, array):
    with open(file, "r") as ins:
        for line in ins:
            array.append(line.replace('\n', '').split(' '))

def searchInArray(a, b, array):
    for i in range(len(array)):
        if(array[i][0] == str(a)):
            if(array[i][0] == str(a) and array[i][1] == str(b)):
                return array[i][2]

def simulation(pp, percentage, net, ranking, run, x1, x2, lp):

    s = 1;
    isInfecting = True

    g = Graph.Read_Ncol('/Users/apple/Desktop/_infa/modelowanie dyfuzji/R/regresja/' + net, directed=False)

    nodes  = Graph.vcount(g)
    print(nodes)
    g.vs["label"] = g.vs["name"]
    numberofseeds = int(round(nodes * percentage, ndigits=0))

    infections = 0

    for i in range(0,nodes):
        g.vs[i]["infected"] = 0
        g.vs[i]["used"] = 0

    #print('LICZBA SEEDOW', numberofseeds)
    for seeds in range(0, numberofseeds):

        #x = g.vs.find(str(seeds))
        #node = int(x.index)

        if (ranking == 'random'):
            node = int(random.uniform(0, nodes))

        g.vs[node]["infected"] = 1
        g.vs[node]["stepinfected"] = 0
        g.vs[node]["used"] = 0
        g.vs[node]["color"] = "green"


    ### ADD LINK TO GRAPH ###
    if(lp == True):
        Graph.add_edge(g, x1, x2);


    x1Degree = Graph.degree(g, g.vs.find(str(x1)))
    x2Degree = Graph.degree(g, g.vs.find(str(x2)))

    sumDegree = x1Degree + x2Degree

    shortestPath = Graph.get_shortest_paths(g, x1, x2)
    shortestPath = len(shortestPath[0])
    closeness = mean(g.closeness())
    transitivity_undirected = mean(g.transitivity_undirected())
    eigenvector_centrality = mean(g.eigenvector_centrality())
    betweenness = mean(g.betweenness())

    ### WRITE TO FILE ###

    while(isInfecting):
        #print("STEP", s)
        infecting = infections
        nodes = Graph.vcount(g)
        for j in range(0,nodes):

            if (g.vs[j]["infected"] == 1 and g.vs[j]["used"] == 0 and g.vs[j]["stepinfected"] != s):
                #print("INFEKUCJĄCY", g.vs[j]['name'])
                g.vs[j]["used"] = 1
                neighborstab = g.neighbors(j, mode="out")

                if (len(neighborstab) > 0):
                    n = 0
                    notinfected = []
                    for i in range (0,len(neighborstab)):
                            if(g.vs[neighborstab[i]]["infected"] == 0):
                                notinfected.append(neighborstab[i])
                    #print(notinfected)
                    numberofneighbors = len(notinfected)

                    if notinfected:
                        for k in range(0,numberofneighbors):
                            if(numberofneighbors >= 1):
                                x = random.random()
                                if(float(x) <= pp):
                                    g.vs[notinfected[k]]["infected"] = 1
                                    g.vs[notinfected[k]]["stepinfected"] = s
                                    g.vs[notinfected[k]]["used"] = 0
                                    g.vs[notinfected[k]]["color"] = "blue"

                                    #print("INFEKCJA",g.vs[j]['name'], g.vs[notinfected[k]]['name'], x, "\n\n")
                                    infections = infections + 1
        if(infecting == infections):
            isInfecting = False

        s = s + 1

        #plot(g)
        #print("Zainfekowanych", infections + numberofseeds)
        #print("Total coverage % (infections + seeds):")
        coverage = 100 * (numberofseeds + infections) / nodes
        return infections + numberofseeds, s - 1, coverage, closeness, transitivity_undirected, eigenvector_centrality, betweenness, shortestPath, sumDegree


#spARR = [0.01, 0.05]
spARR = [0.05]
#ppARR = [0.01, 0.05, 0.1, 0.15, 0.20, 0.25]
ppARR = [0.25]


net = ['16_']
count = 0;

start = time.time()

myFile = open('syntetic/RESULTS/' + net[0][0:3] + 'result.csv', 'a')
with myFile:
    myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'cl', 'cc', 'ev', 'bw', 'sd', 'degree', 'nl']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader();
ranking = ['random']
for k in range(2,100):
    for x1 in range(1, 16):
        for x2 in range(1, 16):
            count = count + 1;
            for n in net:
                n = n + str(k) + '.txt';
                #print(n)
                myFile = open('syntetic/RESULTS/' + n[0:3] + 'result.csv', 'a')
                with myFile:
                    myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'cl', 'cc', 'ev', 'bw', 'sd', 'degree', 'nl']
                    writer = csv.DictWriter(myFile, fieldnames=myFields)
                    for rank in ranking:
                        for sp in spARR:
                            for pp in ppARR:
                                for i in range(1,2):
                                    temp1 = simulation(pp, sp, n, rank, i, x1, x2, False)
                                    temp2 = simulation(pp, sp, n, rank, i, x1, x2, True)
                                    writer.writerow({'ranking': rank, 'run': i, 'net': n, 'sp': sp, 'pp': pp,'step': temp1[1], 'infections': temp1[0], 'coverage': temp1[2],
                                                     'cl': temp1[3], 'cc': temp1[4], 'ev': temp1[5], 'bw': temp1[6], 'sd': 0, 'degree': 0, 'nl': False})
                                    writer.writerow({'ranking': rank, 'run': i, 'net': n, 'sp': sp, 'pp': pp,'step': temp2[1], 'infections': temp2[0], 'coverage': temp2[2],
                                                 'cl': temp2[3], 'cc': temp2[4], 'ev': temp2[5], 'bw': temp2[6], 'sd': temp2[7], 'degree': temp2[8], 'nl': True})


end = time.time()
# print(end - start)
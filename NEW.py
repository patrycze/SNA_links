from igraph import *
import random
# import matplotlib.pyplot as plt
# import numpy as np
# load data into a graph
import csv
import operator
import time
from os import listdir
from os.path import isfile, join


def simulation(pp, net, ranking, run, link, lp, seedsArray):
    # print(seedsArray)
    s = 1;
    isInfecting = True

    g = Graph.Read_Ncol('graphs/' + net, directed=False)

    nodes = Graph.vcount(g)

    g.vs["label"] = g.vs["name"]
    numberofseeds = int(len(seedsArray))
    # print(numberofseeds)
    infections = 0


    for i in range(0, nodes):
        g.vs[i]["infected"] = 0
        g.vs[i]["used"] = 0

    # print('LICZBA SEEDOW', numberofseeds)
    for seeds in seedsArray:
        # print('seeds', seeds)
        x = g.vs.find(str(seeds))
        node = int(x.index)

        g.vs[node]["infected"] = 1
        g.vs[node]["stepinfected"] = 0
        g.vs[node]["used"] = 0
        g.vs[node]["color"] = "green"

    nodeCloseness = 0
    nodeEcc = 0
    nodeBW = 0
    nodeDG = 0
    nodeTR = 0

    closeness = mean(g.closeness())
    transitivity_undirected = mean(g.transitivity_undirected())
    eigenvector_centrality = mean(g.eigenvector_centrality())
    betweenness = mean(g.betweenness())
    assort = 0;
    ### WRITE TO FILE ###

    while (isInfecting):
        # print("STEP", s)
        infecting = infections
        nodes = Graph.vcount(g)
        for j in range(0, nodes):

            if (g.vs[j]["infected"] == 1 and g.vs[j]["used"] == 0 and g.vs[j]["stepinfected"] != s):
                # print("INFEKUCJĄCY", g.vs[j]['name'])
                g.vs[j]["used"] = 1
                neighborstab = g.neighbors(j, mode="out")

                if (len(neighborstab) > 0):
                    n = 0
                    notinfected = []
                    for i in range(0, len(neighborstab)):
                        if (g.vs[neighborstab[i]]["infected"] == 0):
                            notinfected.append(neighborstab[i])
                    # print(notinfected)
                    numberofneighbors = len(notinfected)

                    if notinfected:
                        for k in range(0, numberofneighbors):
                            if (numberofneighbors >= 1):
                                x = random.random()
                                if (float(x) <= pp):
                                    g.vs[notinfected[k]]["infected"] = 1
                                    g.vs[notinfected[k]]["stepinfected"] = s
                                    g.vs[notinfected[k]]["used"] = 0
                                    g.vs[notinfected[k]]["color"] = "blue"
                                    line = "INFEKCJA " + str(g.vs[j]['name']) + ' ' + str(g.vs[notinfected[k]]['name']) + ' ' + str(x) + "\n\n"
                                    # with open("infections.txt", "a") as f:
                                    #         f.write(line)
                                    # print("INFEKCJA",g.vs[j]['name'], g.vs[notinfected[k]]['name'], x, "\n\n")
                                    infections = infections + 1

        if (infecting == infections):
            isInfecting = False

        s = s + 1

        # plot(g)
        # with open("infections.txt", "a") as f:
        #     f.write("Zainfekowanych" + str(infections + numberofseeds) + "\n")
        #print("Zainfekowanych", infections + numberofseeds)
        # print("Total coverage % (infections + seeds):")
        coverage = 100 * (numberofseeds + infections) / nodes
        return infections + numberofseeds, s - 1, coverage, closeness, transitivity_undirected, eigenvector_centrality, betweenness, assort, nodeCloseness, nodeEcc, nodeBW, nodeDG, nodeTR


spARR = [0.1875]
ppARR = [0.1, 0.2, 0.3, 0.4, 0.5]



count = 0;

combinationsArray = []
localMaximum = [];
greedyArray = [];
greedy = 5;
infectionsArray = []


myFile = open('results/results.csv', 'w')
with myFile:
    myFields = ['pp', 'seed', 'coverage', 'net']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader();


graphs = [f for f in listdir('graphs') if isfile(join('graphs', f))]
seeds = [f for f in listdir('seeds') if isfile(join('seeds', f))]

for pp in ppARR:
    for graph in graphs:
        for seed in seeds:
            combinationsArray = []
            print(seed)
            if graph[0] is not '.':
                if int(seed[0]) <= int(graph[0]):
                    with open('seeds/' + seed, "r") as f:
                        for line in f:
                            combinationsArray.append(line)
                        for c in combinationsArray:
                            infectionsArray = []
                            c = c.replace("\n", "").split(" ")
                            print(c)
                            for i in range(1,1000):
                                sim = simulation(pp, graph, 'random', 1, '', False, c)
                                infectionsArray.append(sim[0])
                            infections = mean(infectionsArray)
                            myFile = open('results/results.csv', 'a+')
                            with myFile:
                                myFields = ['pp', 'seed', 'coverage', 'net']
                                writer = csv.DictWriter(myFile, fieldnames=myFields)
                                writer.writerow({'pp': pp,'seed': c, 'coverage': infections, 'net': graph})


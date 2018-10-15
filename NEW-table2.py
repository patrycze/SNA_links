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
import collections

def getLinksArray(net):

    g = Graph.Read_Ncol('graphs-ORIGINAL/' + net, directed=False)

    edges = []

    for e in g.es:
        v1 = g.vs.find(e.source)
        v2 = g.vs.find(e.target)

        if (int(v1['name']) > int(v2['name'])):
            edges.append(str(v2['name']) + '-' + str(v1['name']))
        if (int(v1['name']) < int(v2['name'])):
            edges.append(str(v1['name']) + '-' + str(v2['name']))

            # edges = edges + str(v1['name']) + '-' + str(v2['name']) + ' '

    return edges

def simulation(pp, net, seedsArray):
    # print(seedsArray)
    s = 1;
    isInfecting = True

    g = Graph.Read_Ncol('graphs-ORIGINAL/' + net, directed=False)

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

    # closeness = mean(g.closeness())
    # transitivity_undirected = mean(g.transitivity_undirected())
    # eigenvector_centrality = mean(g.eigenvector_centrality())
    # betweenness = mean(g.betweenness())
    # assort = 0;
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
                                if (float(x) <= float(pp)):
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
        return infections + numberofseeds, s - 1, coverage


spARR = [0.1875]
ppARR = [0.1, 0.2, 0.3, 0.4, 0.5]



count = 0;

combinationsArray = []
localMaximum = [];
greedyArray = [];
greedy = 5;
infectionsArray = []

class NetworkStructure:

    net = ''
    pp = ''
    seed = ''
    addedNetworks = []

listOfNetworks = []

class Network:
    name = ''
    links = []
    coverage = 0

with open('test.csv', "r") as f:
    for line in f:
        combinationsArray.append(line)
    for c in combinationsArray:

        tmpNet = NetworkStructure()
        tmpNet.net = c.split(',')[0]
        tmpNet.pp = c.split(',')[1]


        c = c.replace("\"","")
        c = c.split("[")
        c[1] = c[1].split("]")

        tmpNet.addedNetworks = c[1][1].replace(" ","")[2:].split(",")

        # print(c[1][1].replace(" ","").split(","))
        # print(c[1][1].replace(" ","")[2:].split(","))

        tmpNet.seed = c[1][0].replace('\'',"").replace(' ',"").split(',')

        listOfNetworks.append(tmpNet)

#
# for l in listOfNetworks:
#     for n in l.addedNetworks:
#         if (n.endswith('.txt')):
#             net = Network()
#
#             net.name = n
#             net.coverage
#             net.links = getLinksArray(net.name)
#
#             n = net


myFields = ['net', 'PP', 'seed', 'space', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                '14', '15', '16']

for l in listOfNetworks:
    # print(l.net, l.pp, l.seed, l.addedNetworks)

    infections = []

    # dict = {x: [] for i, x in enumerate(l.addedNetworks) if l.addedNetworks[int(i)].endswith('.txt')}
    # dict = collections.OrderedDict.fromkeys(enumerate(l.addedNetworks))

    dict = collections.OrderedDict.fromkeys(x for i, x in enumerate(l.addedNetworks))

    for key, value in dict.items():
        dict[key] = []

    # print('L.NET', l.addedNetworks)
    # print('DICT', dict)

    # for n in l.addedNetworks:
    for i in range(1, 1000):

        infectionsArray = []

        for n in l.addedNetworks:
            if(n.endswith('.txt')):

                # for i in range(1, 1000):


                sim = simulation(l.pp, l.net, l.seed)
                # infectionsArray.append(sim[0])
                dict[n].append(sim[0])

            if n == '':
                print

    for key, value in dict.items():
        dict[key] = mean(value)

    print("SŁOWNICZEK", dict)

    infections.append(mean(infectionsArray))

    x = {'net': l.net, 'PP': l.pp, 'seed': l.seed, 'space': ' '}
    x1 = {str(i): x for i, x in enumerate(infections)}
    x.update(x1)


    myFile = open('results/results.csv', 'a+')
    with myFile:
        writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
        writer.writerow(x)

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
from collections import Counter
import numpy as np

myFile = open('results/greedy.csv', 'w')
myFile = open('results/results.csv', 'w')
myFile = open('results/max.csv', 'w')

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
    seqFromAddedNetworksGREEDY = []
    seqFromAddedNetworksGREEDYOBJ = []
    seqFromAddedNetworksMAX = []
    seqFromAddedNetworksMAXOBJ = []

    greedySeq = []
    maxSeq = []

listOfNetworks = []

class Network:
    name = ''
    links = []
    coverage = 0
    index = 0

with open('test.csv', "r") as f:
    for line in f:
        combinationsArray.append(line)
    for c in combinationsArray:

        tmpNet = NetworkStructure()
        tmpNet.net = c.split(',')[0]
        # tmpNet.pp = c.split(',')[1]
        tmpNet.pp = 0.5


        c = c.replace("\"","")
        c = c.split("[")
        c[1] = c[1].split("]")

        tmpNet.addedNetworks = c[1][1].replace(" ","")[2:].split(",")

        # print(c[1][1].replace(" ","").split(","))
        # print(c[1][1].replace(" ","")[2:].split(","))

        tmpNet.seed = c[1][0].replace('\'',"").replace(' ',"").split(',')

        listOfNetworks.append(tmpNet)

#
for l in listOfNetworks:
    for i, n in enumerate(l.addedNetworks):
        if (n.endswith('.txt')):
            net = Network()

            net.name = n
            net.index = i
            net.links = getLinksArray(net.name)
            l.addedNetworks[i] = net

myFields = ['net', 'PP', 'seed', 'space', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                '14', '15', '16']

def createMaxSeq(dict, i, collection, quantityOfSeqMAX):

    collectionOfNetwork = []

    for c in collection:
        for n in c:
            if isinstance(n, Network):
                collectionOfNetwork.append(n)
                # print(n.name, n.index)
    try:
        m = max(collectionOfNetwork, key=lambda c: c.index)
        m = m.index + 1
        # print('MAX', m.index)
    except:
        print
        m = 0

    for i in reversed(range(int(m))):
        if(i == m-1):
            pattern = max([n for n in collectionOfNetwork if n.index == i ], key=lambda c: c.coverage)
            # print('PATTERN ', i ,' ', pattern.coverage)
        if i == m-2:
            recSeqNetwork(pattern, collectionOfNetwork, i, quantityOfSeqMAX)
        if m == 1:
            pattern = max([n for n in collectionOfNetwork if n.index == i ], key=lambda c: c.coverage)
            quantityOfSeqMAX.append(pattern)

    # return quantityOfSeq
    # print(i, collection)
def recSeqNetwork(pattern, collectionOfNetwork, i, quantityOfSeqMAX):

    next = filter(lambda x: set(x.links).issubset(set(pattern.links)), [n for n in collectionOfNetwork if n.index == i])
    l = len(pattern.links) - 1
    next = [r for r in next if len(r.links) == l]

    try:

        tmp = Network()

        tmp.links = pattern.links
        tmp.coverage = pattern.coverage
        tmp.index = pattern.index
        tmp.name = pattern.name

        quantityOfSeqMAX.append(tmp)
        # print(i ,' ', random.choice([r.name for r in next]))
        pattern = random.choice([r for r in next])
        recSeqNetwork(pattern, collectionOfNetwork, i-1, quantityOfSeqMAX)
    except:
        print


def createGreedySeq(dict, i, collection, quantityOfSeqGREEDY):

    collectionOfNetwork = []

    for c in collection:
        for n in c:
            if isinstance(n, Network):
                collectionOfNetwork.append(n)
                # print(n.name, n.index)
    try:
        m = max(collectionOfNetwork, key=lambda c: c.index)
        m = m.index + 1
        # print('MAX', m.index)
    except:
        print
        m = 0

    for i in range(int(m)):
            pattern = max([n for n in collectionOfNetwork if n.index == i ], key=lambda c: c.coverage)
            recGreedySeqNetwork(pattern, collectionOfNetwork, i, quantityOfSeqGREEDY)


def recGreedySeqNetwork(pattern, collectionOfNetwork, i, quantityOfSeqGREEDY):

    next = filter(lambda x: set(x.links).issubset(set(pattern.links)), [n for n in collectionOfNetwork if n.index == i])
    l = len(pattern.links) - 1
    next = [r for r in next if len(r.links) == l]

    try:

        tmp = Network()

        tmp.links = pattern.links
        tmp.coverage = pattern.coverage
        tmp.index = pattern.index
        tmp.name = pattern.name

        quantityOfSeqGREEDY.append(tmp)
        print(i ,' ', random.choice([r.name for r in next]))
        pattern = max(next, key=lambda c: c.coverage)
        recGreedySeqNetwork(pattern, collectionOfNetwork, i+1, quantityOfSeqGREEDY)
    except:
        print


def returnNetCollection(net, pp, seed):

    tmpArray = []

    for l in listOfNetworks:
        if(l.net == net and l.pp == pp and l.seed == seed):
            tmpArray.append(l.addedNetworks)

    return tmpArray

selectedNetworks = []

# 42.txt 0.1 ['0']
# 42.txt 0.1 ['0']



for l in listOfNetworks:

    if str(l.net) + str(l.pp) + str(l.seed) not in selectedNetworks:

        selectedNetworks.append(str(l.net) + str(l.pp) + str(l.seed))

        print(l.net, l.pp, l.seed)

        l.seqFromAddedNetworksGREEDY = []
        l.seqFromAddedNetworksGREEDYOBJ = []
        l.seqFromAddedNetworksMAX = []
        l.seqFromAddedNetworksMAXOBJ = []

        infections = []

        # dict = {x: [] for i, x in enumerate(l.addedNetworks) if l.addedNetworks[int(i)].endswith('.txt')}
        # dict = collections.OrderedDict.fromkeys(enumerate(l.addedNetworks))

        dict = collections.OrderedDict.fromkeys(x for i, x in enumerate(l.addedNetworks))

        for key, value in dict.items():
            dict[key] = []

        # print('L.NET', l.addedNetworks)
        # print('DICT', dict)

        # for n in l.addedNetworks:
        # print('ADDED', l.addedNetworks)
        collectionOfNets = returnNetCollection(l.net, l.pp, l.seed)

        for i in range(1, 10):

            infectionsArray = []

            for n in l.addedNetworks:
                if(isinstance(n, Network) and n.name.endswith('.txt')):

                    sim = simulation(l.pp, l.net, l.seed)
                    n.coverage = sim[0]

                    dict[n].append(sim[0])
                    # print('COVERAGE', sim[0])

                if n == '':
                    print


            quantityOfSeqGREEDY = []
            quantityOfSeqMAX = []

            createMaxSeq(dict, i, collectionOfNets, quantityOfSeqMAX)
            createGreedySeq(dict, i, collectionOfNets, quantityOfSeqGREEDY)

            # print('RAW GREEDY', [q.coverage for q in quantityOfSeqGREEDY])

            l.seqFromAddedNetworksGREEDY.append(str(list([q.name for q in quantityOfSeqGREEDY])))
            l.seqFromAddedNetworksGREEDYOBJ.append(quantityOfSeqGREEDY)

            l.seqFromAddedNetworksMAXOBJ.append(list(reversed(quantityOfSeqMAX)))
            l.seqFromAddedNetworksMAX.append(str(list(reversed([q.name for q in quantityOfSeqMAX]))))


        counterGreedy = Counter(l.seqFromAddedNetworksGREEDY)
        counterMax = Counter(l.seqFromAddedNetworksMAX)

        # print([value for key, value in counter.most_common()])
        # print(max(counterMax.most_common(), key=lambda t: t[1])) # CHYBA ZWRACA MAXA
        selectednetMAX = max(counterMax.most_common(), key=lambda t: t[1])

        # print(max(counterGreedy.most_common(), key=lambda t: t[1]), '\n') # CHYBA ZWRACA MAXA
        selectednetGREEDY = max(counterGreedy.most_common(), key=lambda t: t[1])

        # print('SELECTED GREEDY', selectednetGREEDY)
        # print('SELECTED MAX', selectednetMAX)


        averageGreedyArray = np.array([greedyA for greedyA in l.seqFromAddedNetworksGREEDYOBJ if str(list([q.name for q in greedyA])) == selectednetGREEDY[0]]) #SREDNIA Z NAJCZESCIEJ WYSTEPUJACYCH PRZEBIEGOW - ZSUMOWANIE TABLIC Z WYNIKAMI
        averageMaxArray = np.array([maxA for maxA in l.seqFromAddedNetworksMAXOBJ if str(list([m.name for m in maxA])) == selectednetMAX[0]]) #SREDNIA Z NAJCZESCIEJ WYSTEPUJACYCH PRZEBIEGOW - ZSUMOWANIE TABLIC Z WYNIKAMI, NASTEPNY KROK

        averageGreedy = []
        averageMAX = []

        for i in range(0,len(averageGreedyArray[0])):
            print([a.coverage for a in averageGreedyArray[:, i]])
            print(mean([a.coverage for a in averageGreedyArray[:,i]]))
            averageGreedy.append(mean([a.coverage for a in averageGreedyArray[:,i]]))

        for i in range(0, len(averageMaxArray[0])):
            # print([a.coverage for a in averageMaxArray[:, i]])
            # print(mean([a.coverage for a in averageMaxArray[:, i]]))
            averageMAX.append(mean([a.coverage for a in averageMaxArray[:, i]]))

        for key, value in dict.items():
            dict[key] = mean(value)


        # infections.append(mean(infectionsArray))

        x = {'net': l.net, 'PP': l.pp, 'seed': l.seed, 'space': ' '}
        tmp = [value for key, value in dict.items()]
        x1 = {str(i): x for i, x in enumerate(tmp)}
        x.update(x1)




        myFile = open('results/results.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow(x)

        x = {'net': l.net, 'PP': l.pp, 'seed': l.seed, 'space': ' '}
        tmp = [value for key, value in dict.items()]
        x1 = {str(i): x for i, x in enumerate(averageMAX)}
        x.update(x1)

        myFile = open('results/max.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow(x)

        x = {'net': l.net, 'PP': l.pp, 'seed': l.seed, 'space': ' '}
        tmp = [value for key, value in dict.items()]
        x1 = {str(i): x for i, x in enumerate(averageGreedy)}
        x.update(x1)

        myFile = open('results/greedy.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow(x)

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
import os


from os import listdir
from os.path import isfile, join


myFile = open('results/averageGREEDY.csv', 'w')


def readFileToArray(file, array):
    # print(file)
    with open(file, "r") as ins:
        for line in ins:
            array.append(line.replace('\n', '').split(' '))

def searchInArray(a, b, array):
    for i in range(len(array)):
        if(array[i][0] == str(a) and array[i][1] == str(b)):
            #print(array[i][0], array[i][1], array[i][2])
            return array[i][2]

myFile = open('results/tabl2.csv', 'w')


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

def simulation(pp, net, seedsArray, i):
    # print(seedsArray)
    s = 1;
    isInfecting = True

    array = []

    readFileToArray('wagi/n1_' + str(i) + '.txt', array)

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
                                # x = random.random()
                                x = searchInArray(g.vs[j]['name'], g.vs[notinfected[k]]['name'], array)

                                if (float(x) <= float(pp)):
                                    g.vs[notinfected[k]]["infected"] = 1
                                    g.vs[notinfected[k]]["stepinfected"] = s
                                    g.vs[notinfected[k]]["used"] = 0
                                    g.vs[notinfected[k]]["color"] = "blue"
                                    line = "INFEKCJA " + str(g.vs[j]['name']) + ' ' + str(g.vs[notinfected[k]]['name']) + ' ' + str(x) + "\n\n"
                                    infections = infections + 1

        if (infecting == infections):
            isInfecting = False

        s = s + 1

        coverage = 100 * (numberofseeds + infections) / nodes
        return infections + numberofseeds, s - 1, coverage, net, pp


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
    seqFromAddedNetworksRANDOM = []
    seqFromAddedNetworksRANDOMOBJ = []

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
        tmpNet.pp = c.split(',')[1]


        c = c.replace("\"","")
        c = c.split("[")
        c[1] = c[1].split("]")

        tmpNet.addedNetworks = c[1][1].replace(" ","")[2:].split(",")

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
        if (n == ''):
            n = 'space_' + str(i);
            l.addedNetworks[i] = n

myFields = ['net', 'PP', 'seed', 'space', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                '14', '15', '16']

myFields1 = ['inf','seed','cov','net', 'pp']
def createRandomSeq(dict, i, collection, quantityOfSeqRandom):

    collectionOfNetwork = []

    for c in collection:
        for n in c:
            if isinstance(n, Network):
                collectionOfNetwork.append(n)

    try:
        m = max(collectionOfNetwork, key=lambda c: c.index)
        m = m.index + 1
    except:
        print
        m = 0

    for i in range(int(m)):
        pattern = random.choice([n for n in collectionOfNetwork if n.index == i])

        tmp = Network()

        tmp.links = pattern.links
        tmp.coverage = pattern.coverage
        tmp.index = pattern.index
        tmp.name = pattern.name

        quantityOfSeqRandom.append(tmp)


def createMaxSeq(collection, quantityOfSeqMAX):
    collectionOfNetwork = []

    for c in collection:
        for n in c:
            if isinstance(n, Network):
                collectionOfNetwork.append(n)

    try:
        m = max(collectionOfNetwork, key=lambda c: c.index)
        m = m.index + 1
    except:
        print
        m = 0

    for i in range(int(m)):
        pattern = max([n for n in collectionOfNetwork if n.index == i], key=lambda c: c.coverage)

        tmp = Network()

        tmp.links = pattern.links
        tmp.coverage = pattern.coverage
        tmp.index = pattern.index
        tmp.name = pattern.name

        quantityOfSeqMAX.append(tmp)

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
        pattern = random.choice([r for r in next])
        recSeqNetwork(pattern, collectionOfNetwork, i-1, quantityOfSeqMAX)
    except:
        print


def createGreedySeq(i, collection, quantityOfSeqGREEDY):

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

    pattern = max([n for n in collectionOfNetwork if n.index == 0], key=lambda c: c.coverage)

    recGreedySeqNetwork(pattern, collectionOfNetwork, i, quantityOfSeqGREEDY)

def checkExist(net, pp, seedArray):
    onlyfiles = [f for f in listdir('resultsPerNet') if isfile(join('resultsPerNet', f))]
    print('PLIKI',onlyfiles)
    print('SPRAWDZAM PLIK', net)
    if net in onlyfiles:
        statinfo = os.stat('resultsPerNet/' + net)
        print('ROZMIAR', statinfo.st_size)

    if net not in onlyfiles:
        return False

def recGreedySeqNetwork(pattern, collectionOfNetwork, i, quantityOfSeqGREEDY):

    tmp = Network()
    tmp.links = pattern.links
    tmp.coverage = pattern.coverage
    tmp.index = pattern.index
    tmp.name = pattern.name
    quantityOfSeqGREEDY.append(tmp)


    next = list(filter(lambda x: set(pattern.links).issubset(set(x.links)), [n for n in collectionOfNetwork if n.index == i]))

    l = len(pattern.links) + 1
    next = [r for r in next if len(r.links) == l]


    try:
        pattern = max(next, key=lambda c: c.coverage)

        recGreedySeqNetwork(pattern, collectionOfNetwork, i+1, quantityOfSeqGREEDY)
    except:
        print


def returnNetCollection(net, pp, seed):

    tmpArray = []

    for l in listOfNetworks:
        if(l.net == net and l.pp == pp and l.seed == seed):
            if(len(tmpArray) > 0):
                tmpArray.append(l.addedNetworks[1:])
            else:
                tmpArray.append(l.addedNetworks)

    return tmpArray

selectedNetworks = []
existList = []

for l in listOfNetworks:
        print('NOWY PRZEBIEG', l.net, [n.name for n in l.addedNetworks if isinstance(n,Network)])
        l.seqFromAddedNetworksGREEDY = []
        l.seqFromAddedNetworksMAX = []
        l.seqFromAddedNetworksRANDOM = []

        infections = []

        # print([f for i, f in enumerate(l.addedNetworks)])
        dict = collections.OrderedDict.fromkeys(x for i, x in enumerate(l.addedNetworks))
        # print(dict.items())
        for key, value in dict.items():
            dict[key] = []


        collectionOfNets = returnNetCollection(l.net, l.pp, l.seed)

        # restOfNetworks = list(set([net.name
        #                         for collection in collectionOfNets
        #                             for net in collection if isinstance(net, Network)
        #                                     ]) - set([net.name for net in l.addedNetworks if isinstance(net, Network)]))


        for n in l.addedNetworks:
            if isinstance(n, Network):
                print(n.name)
                infectionsArray = []
                first = False

                if(isinstance(n, Network) and n.name.endswith('.txt')):
                    row = str(l.pp) + ' ' +  str(n.name) + ' ' +  str(l.seed)
                    print('ROW', row)

                    for i in range(1, 1000):

                        sim = simulation(l.pp, n.name, l.seed, i)   # zmiana z l na n
                        n.coverage = sim[0]

                        dict[n].append(sim[0])
                        # flag = checkExist(n.name)
                        # print(flag)
                        if row not in existList or first == True:
                            existList.append(row)
                            first = True
                            myFile = open('resultsPerNet/' + sim[3] + '_' + str(l.pp) + '_' + str(l.seed) + '.txt', 'a+')
                            with myFile:
                                writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields1, extrasaction='ignore')
                                writer.writerow({'inf': sim[0],'seed': sim[1],'cov': sim[2],'net': n.name, 'pp': sim[4]})

                        if n == '':
                            print

                    # flag = checkExist(l.net + '.txt')

                    # print('INFECTED', sim)


        for key, value in dict.items():
            dict[key] = mean(value)

        x = {'net': l.net, 'PP': l.pp, 'seed': l.seed, 'space': ' '}
        tmp = [value for key, value in dict.items()]
        x1 = {str(i): x for i, x in enumerate(tmp)}
        x.update(x1)
        print(x)
        myFile = open('results/averageGREEDY.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow(x)

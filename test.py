from igraph import *
import random
# import pandas
from collections import Counter
# import matplotlib.pyplot as plt
# import numpy as np
# load data into a graph
import csv
import operator
import time
import collections
import re

d = collections.defaultdict(list)



def removeFromGraph(graph, link):
    # Graph.get.edge.ids(g, link[i], link[i + 1]);
    edge = graph.get_eid(link[0], link[1])
    # print(edge)
    Graph.delete_edges(graph, edge)
def readFileToArray(file, array):
    with open(file, "r") as ins:
        for line in ins:
            array.append(line.replace('\n', '').split(' '))


def searchInArray(a, b, array):
    # print('array', array)
    for i in range(len(array)):
        if (array[i][0] == str(a)):
            if (array[i][0] == str(a) and array[i][1] == str(b)):
                return array[i][2]

def addLinksToGraph(g, arr):
    for i in range(0, len(arr), 2):
        try:
            Graph.add_edge(g, arr[i], arr[i + 1]);
            # print(arr[i], arr[i + 1])
        except ValueError:
            print('')


def closenessForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.closeness(g, [g.vs.find(arr[i]), g.vs.find(arr[i + 1])])
            measuresArray.append(mean(m));
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));

    return measuresArray


def eccentricityForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.eccentricity(g, [g.vs.find(arr[i]), g.vs.find(arr[i + 1])])
            measuresArray.append(mean(m))
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray


def betweennessForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.betweenness(g, [g.vs.find(arr[i]), g.vs.find(arr[i + 1])])
            measuresArray.append(mean(m));
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray

def searchInArray(a, b, array):
    for i in range(len(array)):
        if(array[i][0] == str(a)):
            if(array[i][0] == str(a) and array[i][1] == str(b)):
                return array[i][2]
        if (array[i][1] == str(a)):
            if(array[i][1] == str(a) and array[i][0] == str(b)):
                return array[i][3]


def degreeForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.degree(g, [g.vs.find(arr[i]), g.vs.find(arr[i + 1])])
            measuresArray.append(mean(m));
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray


def transitivityForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.transitivity_local_undirected(g, [g.vs.find(arr[i]), g.vs.find(arr[i + 1])])
            measuresArray.append(mean(m))
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray


def addToGraphGreedyLinks(g, greedyArray):
    for i in range(0, len(greedyArray)):
        if not (g.are_connected(greedyArray[i][0], greedyArray[i][1])):
            try:
                Graph.add_edge(g, greedyArray[i][0], greedyArray[i][1]);
                # print(arr[i], arr[i + 1])
            except ValueError:
                print('')

def removeFromArray(link, array, greedyArray):
    array[:] = [d for d in array if d.get('pair') != link]
    if(link in greedyArray) and any(d.get('pair', None) == link for d in array):
        removeFromArray(link, array, greedyArray)
    else:
        return array

def simulation(pp, percentage, net, ranking, run, link, lp, greedyArray, graph, readArray):
    # print(link)
    s = 1;
    isInfecting = True
    # path = 'C:\\Users\\Patryk\\Desktop\\SNA_links\\nets\\' + net;
    # print(path)
    g = graph;
    nodes = Graph.vcount(g)
    # print(len(g.es))
    # if (len(greedyArray) > 0):
        # print('GREEDY ARRAY IN SIMULATION ', greedyArray);

    array = readArray;



    if (lp == True):
        addLinksToGraph(g, link)

    addToGraphGreedyLinks(g, greedyArray);
    # print(len(g.es))
    #for e in g.es:
        #print(g.vs[e.source], g.vs[e.target])

    g.vs["label"] = g.vs["name"]
    # numberofseeds = int(round(nodes * percentage, ndigits=0))
    numberofseeds = 1

    infections = 0

    #### DEGREE ####

    if (ranking == 'degree'):
        d = g.degree(mode="out");
        g.vs['degree'] = d
        m = sorted(g.vs, key=lambda x: x['degree'], reverse=True)
        # for e in m:
        # print(e)

    ### BETWEENNESS ###

    if (ranking == 'betweenness'):
        b = g.betweenness()
        g.vs['between'] = b
        m = sorted(g.vs, key=lambda z: z['between'], reverse=True)

    ### EIGENVECTOR ###

    if (ranking == 'eigenvector'):
        d = g.evcent()
        g.vs['eigenvector'] = d
        m = sorted(g.vs, key=lambda z: z['eigenvector'], reverse=True)

    for i in range(0, nodes):
        g.vs[i]["infected"] = 0
        g.vs[i]["used"] = 0

    # print('LICZBA SEEDOW', numberofseeds)
    for seeds in range(0, numberofseeds):

        # x = g.vs.find(str(seeds))
        # node = int(x.index)

        if (ranking == 'degree' or ranking == 'betweenness' or ranking == 'eigenvector'):
            node = m[seeds].index
        if (ranking == 'random'):
            node = int(random.uniform(0, nodes))

        g.vs[node]["infected"] = 1
        g.vs[node]["stepinfected"] = 0
        g.vs[node]["used"] = 0
        g.vs[node]["color"] = "green"

    nodeCloseness = 0
    nodeEcc = 0
    nodeBW = 0
    nodeDG = 0
    nodeTR = 0
    ### ADD LINK TO GRAPH ###
    if (lp == True):
        # addLinksToGraph(g, link)
        nodeCloseness = 0
        # nodeCloseness = closenessForNodes(g, link)
        nodeEcc = 0
        # nodeEcc = eccentricityForNodes(g, link)
        nodeBW = 0
        # nodeBW = betweennessForNodes(g, link)
        nodeDG = 0
        #nodeDG = degreeForNodes(g, link)
        nodeTR = 0
        #nodeTR = transitivityForNodes(g, link)
    # x1Degree = Graph.degree(g, g.vs.find(str(x1)))
    # x2Degree = Graph.degree(g, g.vs.find(str(x2)))

    # sumDegree = x1Degree + x2Degree

    # shortestPath = Graph.get_shortest_paths(g, x1, x2)
    # shortestPath = len(shortestPath[0])
    # closeness = mean(g.closeness())
    closeness = 0
    # transitivity_undirected = mean(g.transitivity_undirected())
    transitivity_undirected = 0
    # eigenvector_centrality = mean(g.eigenvector_centrality())
    eigenvector_centrality = 0
    # eigenvector_centrality = 0
    betweenness = 0
    # betweenness = mean(g.betweenness())
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
                                x = searchInArray(g.vs[j]['name'], g.vs[notinfected[k]]['name'], array)
                                if(x == None):
                                    # x = random.randint(0,1)
                                    x = random.uniform(0.01,1.00)
                                    # x = 0.01
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
                                    # print('stop')
                                        # plot(g)

        if (infecting == infections):
            isInfecting = False

        s = s + 1

        # plot(g)
        if(lp == True):
            removeFromGraph(g, link)
        # with open("infections.txt", "a") as f:
        #     f.write("Zainfekowanych" + str(infections + numberofseeds) + "\n")
        # print("Zainfekowanych", infections + numberofseeds)
        # print("Total coverage % (infections + seeds):")
        coverage = 100 * (numberofseeds + infections) / nodes
        return infections + numberofseeds, s - 1, coverage, closeness, transitivity_undirected, eigenvector_centrality, betweenness, assort, nodeCloseness, nodeEcc, nodeBW, nodeDG, nodeTR


spARR = [0.1875]
# spARR = [0.1875, 0.125, 0.0625]
#ppARR = [0.5]
ppARR = [0.1]

# net = ['ba1.5', 'ba1.9', 'ba2.3', 'ba2.7', 'ba3.1', 'ba3.5', 'ba3.9',
#       'er_16_16', 'er_16_32', 'er_16_48', 'er_16_64', 'er_16_80',
#       'ws_2_0', 'ws_2_0.25', 'ws_2_0.5', 'ws_2_0.75', 'ws_2_1',
#       'ws_4_0', 'ws_4_0.25', 'ws_4_0.5', 'ws_4_0.75', 'ws_4_1']

net = ['ba1.5']

count = 0;

combinationsArray = []

# for e in g.es:
    # print(e.target)

start = time.time()
localMaximum = [];
greedyArray = [];
greedy = 2;
stuff = [];

with open("fileGreedy.txt", "r") as f:
    for line in f:
        combinationsArray.append(line.replace("\n", "").split(" "))
localMaximum.append({'pair': combinationsArray[1], 'coverage': 0})
iterarr = [x * 0.1 for x in range(11,12)]
for iter in iterarr:
    for type in range(1,2):
        if(iter == 2.0 or iter == 3.0 or iter == 4.0 or iter == 5.0):
            iter = iter + 0.1
        net = 'ba' + str(type) + '_' + str(iter)[0:3]
        g = Graph.Read_Ncol('C:\\Users\\Patryk\\Desktop\\SNA_links\\nets\\' + net + '.txt', directed=False)
        reset = g;
        network = 'ba_' + net
        toanalysis = [];
        greedyAnalysis = [];
        # ranking = ['random', 'degree', 'betweenness', 'eigenvector']
        ranking = ['degree']
        array = [];
        print('SIEĆ', iter)
        print('')
        for rank in ranking:
            for sp in spARR:
                for pp in ppARR:
                    greedyArray = [];
                    for greedy in range(1,5):
                        localMaximum = []
                        sorted_by_value = []
                        toanalysis = []
                        stuff = []
                        print('GREEDY ARRAY **************', greedyArray)
                        for i in range(1, 100):
                            infectionsArray = []
                            array = [];
                            for link in combinationsArray:
                                readFileToArray('C:\\Users\\Patryk\\Desktop\\SNA_links\\nets\\networks\\' + net + '_' + str(i) + '.txt', array)
                                temp2 = simulation(pp, sp, network, rank, i, link, True, greedyArray, g, array)
                                infectionsArray.append(temp2[0])
                                localMaximum.append({'pair': link, 'coverage': temp2[0]});
                                stuff.append({'pair': link, 'coverage': temp2[0]});

                            sorted_by_value = sorted(localMaximum, key=lambda k: k['coverage'], reverse=True)
                            # print(sorted_by_value)
                            maximum = sorted_by_value[0]['coverage']
                            # print(maximum)
                            # print(sorted_by_value)
                            for i in range(0,len(localMaximum)):
                                if (sorted_by_value[i]['coverage'] == maximum):
                                    toanalysis.append(str(sorted_by_value[i]['pair']) + ', ' + str(greedyArray))

                        for s in stuff:
                           d[str(s["pair"])].append(int(s["coverage"]))

                        # print(d.items())
                        result = {k: sum(v) / len(v) for k, v in d.items()}
                        sorted_x = sorted(result.items(), key=operator.itemgetter(1), reverse=True)

                        for key in sorted_x:
                            print('MAXIMUM PAIR **************', key[0])
                            if not (key[0].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',') in greedyArray):
                                print(key[0].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(','))
                                greedyArray.append(key[0].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(','));
                                break

                        print('RAW ARRAY WITH COVERAGE ***', sorted_by_value)
                        print('ANALYSIS ******************', toanalysis)
                        print('ANALYSIS ******************', Counter(toanalysis))
                        print('DATA FRAME', sorted_x)

                        print('')

                        myFile = open('results/' + 'resultsRawArray.csv', 'a')
                        with myFile:
                            myFields = ['pair', 'coverage']
                            writer = csv.DictWriter(myFile, fieldnames=myFields)
                            writer.writeheader();
                            for line in sorted_by_value:
                                writer.writerow(
                                    {'pair': line['pair'],
                                     'coverage': line['coverage'] })

                        # myFile = open('results/' + 'resultsWithMaxValue.csv', 'a')
                        # with myFile:
                        #     myFields = ['pair', 'coverage']
                        #     writer = csv.DictWriter(myFile, fieldnames=myFields)
                        #     writer.writeheader();
                        #     for line in toanalysis:
                        #         print(re.search("^'pair'://.*,$", line).group(0))
                        #         writer.writerow(
                        #             {'pair': line['pair'],
                        #              'coverage': line['coverage']})

                        # myFile = open('results/' + 'resultsMaxValueWithQuantity.csv', 'a')
                        # with myFile:
                        #     myFields = ['pair', 'coverage']
                        #     writer = csv.DictWriter(myFile, fieldnames=myFields)
                        #     writer.writeheader();
                        #     for line in Counter(toanalysis):
                        #         writer.writerow(
                        #             {'pair': line['pair'],
                        #              'coverage': line['coverage']})


        # end = time.time()
        # print(end - start)

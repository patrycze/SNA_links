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

def addLinksToGraph(g, arr):
    for i in range(0,len(arr),2):
        try:
            Graph.add_edge(g, arr[i], arr[i + 1]);
            #print(arr[i], arr[i + 1])
        except ValueError:
            print('')

def closenessForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):

        try:
            m = Graph.closeness(g, [g.vs.find(arr[i]), g.vs.find(arr[i+1])])
            measuresArray.append(mean(m));
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));

    return measuresArray

def eccentricityForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.eccentricity(g, [g.vs.find(arr[i]), g.vs.find(arr[i+1])])
            measuresArray.append(mean(m))
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray

def betweennessForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.betweenness(g, [g.vs.find(arr[i]), g.vs.find(arr[i+1])])
            measuresArray.append(mean(m));
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray

def degreeForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.degree(g, [g.vs.find(arr[i]), g.vs.find(arr[i+1])])
            measuresArray.append(mean(m));
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray


def transitivityForNodes(g, arr):
    measuresArray = [];
    for i in range(0, len(arr), 2):
        try:
            m = Graph.transitivity_local_undirected(g, [g.vs.find(arr[i]), g.vs.find(arr[i+1])])
            measuresArray.append(mean(m))
        except ValueError:
            m = 0;
            measuresArray.append(mean(m));
    return measuresArray

def simulation(pp, percentage, net, ranking, run, link, lp):

    #print(link)
    s = 1;
    isInfecting = True

    g = Graph.Read_Ncol('/Users/apple/Desktop/nets/' + net, directed=False)

    nodes  = Graph.vcount(g)

    #for e in g.es:
    #    print(e.source, e.target)

    g.vs["label"] = g.vs["name"]
    numberofseeds = int(round(nodes * percentage, ndigits=0))

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
    if(lp == True):
        addLinksToGraph(g, link)
        nodeCloseness = closenessForNodes(g, link)
        nodeEcc = eccentricityForNodes(g, link)
        nodeBW = betweennessForNodes(g, link)
        nodeDG = degreeForNodes(g, link)
        nodeTR = transitivityForNodes(g, link)
    #x1Degree = Graph.degree(g, g.vs.find(str(x1)))
    #x2Degree = Graph.degree(g, g.vs.find(str(x2)))

    #sumDegree = x1Degree + x2Degree

    #shortestPath = Graph.get_shortest_paths(g, x1, x2)
    #shortestPath = len(shortestPath[0])
    closeness = mean(g.closeness())
    transitivity_undirected = mean(g.transitivity_undirected())
    eigenvector_centrality = mean(g.eigenvector_centrality())
    betweenness = mean(g.betweenness())
    assort = 0;
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
                                    #line = "INFEKCJA " + str(g.vs[j]['name']) + ' ' + str(g.vs[notinfected[k]]['name']) + ' ' + str(x) + "\n\n"
                                    #with open("infections.txt", "a") as f:
                                    #        f.write(line)
                                    #print("INFEKCJA",g.vs[j]['name'], g.vs[notinfected[k]]['name'], x, "\n\n")
                                    infections = infections + 1
                                    if(infections == 17):
                                        print('stop')

        if(infecting == infections):
            isInfecting = False

        s = s + 1

        plot(g)
        #with open("infections.txt", "a") as f:
        #    f.write("Zainfekowanych" + str(infections + numberofseeds) + "\n")
        #print("Zainfekowanych", infections + numberofseeds)
        #print("Total coverage % (infections + seeds):")
        coverage = 100 * (numberofseeds + infections) / nodes
        return infections + numberofseeds, s - 1, coverage, closeness, transitivity_undirected, eigenvector_centrality, betweenness, assort, nodeCloseness, nodeEcc, nodeBW, nodeDG, nodeTR


spARR = [0.1875]
#spARR = [0.1875, 0.125, 0.0625]
#ppARR = [0.1, 0.2, 0.3, 0.4, 0.5]
ppARR = [0.5]


#net = ['ba1.5', 'ba1.9', 'ba2.3', 'ba2.7', 'ba3.1', 'ba3.5', 'ba3.9',
#       'er_16_16', 'er_16_32', 'er_16_48', 'er_16_64', 'er_16_80',
#       'ws_2_0', 'ws_2_0.25', 'ws_2_0.5', 'ws_2_0.75', 'ws_2_1',
#       'ws_4_0', 'ws_4_0.25', 'ws_4_0.5', 'ws_4_0.75', 'ws_4_1']

net = ['ba1.5']

count = 0;

combinationsArray = []

#start = time.time()

with open("file.txt", "r") as f:
  for line in f:
      combinationsArray.append(line.replace("\n", "").split(" "))


myFile = open('syntetic/RESULTS/' + net[0][0:5] + 'result.csv', 'a')
with myFile:
    myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'cl', 'cc', 'ev', 'bw', 'assort', 'closenessV1', 'closenessV2', 'eccV1', 'eccV2', 'bwV1', 'bwV2', 'dgV1', 'dgV2', 'trV1', 'trV2', 'nl']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader();
ranking = ['random', 'degree', 'betweenness', 'eigenvector']
#ranking = ['random']

for rank in ranking:
    for sp in spARR:
        for pp in ppARR:
            for i in range(1,2):
                for n in net:
                    n = n + '.txt';
                    temp1 = simulation(pp, sp, n, rank, i, '', False)
                    myFile = open('syntetic/RESULTS/' + n[0:5] + 'result.csv', 'a')
                    with myFile:
                        myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'cl',
                                    'cc', 'ev', 'bw', 'assort', 'closenessV1', 'closenessV2', 'eccV1', 'eccV2', 'bwV1', 'bwV2', 'dgV1', 'dgV2', 'trV1', 'trV2', 'nl']
                        writer = csv.DictWriter(myFile, fieldnames=myFields)
                        writer.writerow({'ranking': rank, 'run': i, 'net': n, 'sp': sp, 'pp': pp, 'step': temp1[1],
                                         'infections': temp1[0], 'coverage': temp1[2],
                                         'cl': temp1[3], 'cc': temp1[4], 'ev': temp1[5], 'bw': temp1[6], 'assort': temp1[7], 'closenessV1': temp1[8], 'closenessV2': temp1[8],
                                             'eccV1': temp1[9], 'eccV2': temp1[9], 'bwV1': temp1[10], 'bwV2': temp1[10], 'dgV1': temp1[11], 'dgV2': temp1[11], 'trV1': temp1[12], 'trV2': temp1[12], 'nl': False})
                    for link in combinationsArray:
                        temp2 = simulation(pp, sp, n, rank, i, link, True)
                        myFile = open('syntetic/RESULTS/' + n[0:5] + 'result.csv', 'a+')
                        with myFile:
                            myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'cl',
                                        'cc', 'ev', 'bw', 'assort', 'closenessV1', 'closenessV2', 'eccV1',
                                        'eccV2', 'bwV1', 'bwV2', 'dgV1', 'dgV2', 'trV1', 'trV2', 'nl']
                            writer = csv.DictWriter(myFile, fieldnames=myFields)
                            writer.writerow({'ranking': rank, 'run': i, 'net': n, 'sp': sp, 'pp': pp,'step': temp2[1], 'infections': temp2[0], 'coverage': temp2[2],
                                         'cl': temp2[3], 'cc': temp2[4], 'ev': temp2[5], 'bw': temp2[6], 'assort': temp1[7], 'closenessV1': temp2[8][0], 'closenessV2': temp2[8][1],
                                             'eccV1': temp2[9][0], 'eccV2': temp2[9][1], 'bwV1': temp2[10][0], 'bwV2': temp2[10][1], 'dgV1': temp2[11][0], 'dgV2': temp2[11][1], 'trV1':  temp2[12][0], 'trV2':  temp2[12][1], 'nl': True})


#end = time.time()
#print(end - start)
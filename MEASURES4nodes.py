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


def prepateDifferenceFormat(difference):
    return difference.replace("[","").replace("]","").replace("'","").split("-")

def simulation(net, difference):

    g = Graph.Read_Ncol('C:/Users/Patryk/Desktop/SNA_Links/SNA_links/graphs/' + net, directed=False)

    v1 = ''
    v2 = ''

    closeness = 0
    betweenness = 0
    degree = 0

    if difference != ['']:
        for v in g.vs:
            if (v['name'] == difference[0]):
                v1 = v.index
            if (v['name'] == difference[1]):
                v2 = v.index

        closeness = g.closeness(vertices=[v1, v2])
        betweenness = g.betweenness(vertices=[v1, v2])
        degree = g.degree(vertices=[v1, v2])

        # print('CLOSENES', closeness)
        # print('BETWEENNESS', betweenness)
        # print('DEGREEE', degree)


    # nodes = Graph.vcount(g)
    # edges = ''


    # transitivity_undirected = mean(g.transitivity_undirected())
    # eigenvector_centrality = mean(g.eigenvector_centrality())
    # betweenness = mean(g.betweenness())
    # assort = 0;

    return closeness, betweenness, degree

def readListWithSeq(name, list):
    with open('greedy-OP/' + name + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row != []:
                if row[0] != 'net':
                    list.append(
                        {'net': row[0], 'coverage': row[1], 'edges': row[2], 'increase': row[3], 'difference': row[4],
                         'closeness': row[5], 'transitivity': row[6], 'eigenvector': row[7], 'betweenness': row[8]})


greedySeqList = []
maxSeqList = []
randomSeqList = []

randNets = []

readListWithSeq('listOfDifferencesInGreedy', greedySeqList)
readListWithSeq('listOfDifferencesInRandom', maxSeqList)
# readListWithSeq('listOfDifferencesInMax', randomSeqList)

for i in range (0,len(greedySeqList)):
    # randNets.append(greedySeqList[i+1]['net'])
    # print(g)
    temp = simulation(greedySeqList[i+1]['net'], prepateDifferenceFormat(greedySeqList[i]['difference']))
    randNets.append({'net': greedySeqList[i]['net'], 'coverage': greedySeqList[i]['coverage'], 'edges': greedySeqList[i]['edges'],
                     'increase': greedySeqList[i]['increase'], 'difference': greedySeqList[i]['difference'],
                         'closeness': greedySeqList[i]['closeness'], 'transitivity': greedySeqList[i]['transitivity'],
                     'eigenvector': greedySeqList[i]['eigenvector'], 'betweenness': greedySeqList[i]['betweenness'],
                     'closeness': temp[0]})
    print(randNets[i])

# print(randNets)
# for i in range(0, len(randNets)):
#     print(i+1)
#     simulation(randNets[i+1]['net'], prepateDifferenceFormat(randNets[i]['difference']))

# myFile = open('results/graphs.csv', 'w')
# with myFile:
#     myFields = ['net', 'nodes', 'edges', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
#     writer = csv.DictWriter(myFile, fieldnames=myFields)
#     writer.writeheader();


# graphs = [f for f in listdir('graphs') if isfile(join('graphs', f))]
#
# edges = []

### LECI SYMULACJA

# for graph in graphs:
#     if graph[0] is not '.':
#         sim = simulation(graph)
#         myFile = open('results/graphs.csv', 'a+')
#         with myFile:
#             myFields = ['net', 'nodes', 'edges', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
#             writer = csv.DictWriter(myFile, fieldnames=myFields)
#             edges.append(sim[1])
#             writer.writerow({'net': graph, 'nodes': sim[0], 'edges': sim[1], 'closeness': sim[2], 'transitivity': sim[3],
#                              'eigenvector': sim[4], 'betweenness': sim[5]})


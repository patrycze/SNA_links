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


def simulation(net):

    g = Graph.Read_Ncol('graphs/' + net, directed=False)

    nodes = Graph.vcount(g)
    edges = ''

    for e in g.es:
        # print(e.source, e.target)
        edges = edges + str(e.source) + '-' + str(e.target) + ' '

    closeness = mean(g.closeness())
    transitivity_undirected = mean(g.transitivity_undirected())
    eigenvector_centrality = mean(g.eigenvector_centrality())
    betweenness = mean(g.betweenness())
    assort = 0;

    return nodes, edges, closeness, transitivity_undirected, eigenvector_centrality, betweenness



myFile = open('results/graphs.csv', 'w')
with myFile:
    myFields = ['net', 'nodes', 'edges', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader();


graphs = [f for f in listdir('graphs') if isfile(join('graphs', f))]

edges = []

for graph in graphs:
    if graph[0] is not '.':
        sim = simulation(graph)
        print(sim)
        myFile = open('results/graphs.csv', 'a+')
        with myFile:
            myFields = ['net', 'nodes', 'edges', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            edges.append(sim[1])
            writer.writerow({'net': graph, 'nodes': sim[0], 'edges': sim[1], 'closeness': sim[2], 'transitivity': sim[3],
                             'eigenvector': sim[4], 'betweenness': sim[5]})

def checkIfExist(edge):
    edge = edge[:-4]
    if any(edge == s for s in edges) and len(edge) >= 3:
        # print(edge)
        result.append(edge)
        checkIfExist(edge)

result = []

for x in range (0, len(edges)):
    edges[x] = edges[x][:-1]
    # print(edges[x])


for edge in edges:
    result.append(edge)
    checkIfExist(edge)

for x in result:
    print(x)
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

        eccentricity1 = Graph.eccentricity(g, [e.source])
        closeness1 = Graph.closeness(g, [e.source])
        betweenness1 = Graph.betweenness(g, [e.source])
        degree1 = Graph.degree(g, [e.source])
        eccentricity2 = Graph.eccentricity(g, [e.target])
        closeness2 = Graph.closeness(g, [e.target])
        betweenness2 = Graph.betweenness(g, [e.target])
        degree2 = Graph.degree(g, [e.target])

        myFile = open('results/nodes.csv', 'a+')
        with myFile:
            myFields = ['net', 'node', 'closeness', 'eccentricity', 'degree', 'betweenness']
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writerow(
                {'net': net,  'node': e.source, 'closeness': closeness1, 'eccentricity': eccentricity1, 'degree': degree1, 'betweenness': betweenness1})
            writer.writerow(
                {'net': net,  'node': e.target, 'closeness': closeness2, 'eccentricity': eccentricity2, 'degree': degree2, 'betweenness': betweenness2})


myFile = open('results/nodes.csv', 'w')
with myFile:
    myFields = ['net', 'node', 'closeness', 'eccentricity', 'degree', 'betweenness']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader();


graphs = [f for f in listdir('graphs') if isfile(join('graphs', f))]

for graph in graphs:
    if graph[0] is not '.':
        sim = simulation(graph)



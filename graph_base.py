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

# for x in result:
    # print(x)
results = []
links = []

with open('results/resultWithE.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # print(row)
        if row != []:
            results.append({'net': row[0],'coverage': row[1], 'links': row[3]})


# for x in results:
    # print(x['links'])

with open('results/links.txt', 'r') as txtfile:
    reader = csv.reader(txtfile)
    for row in reader:
        links.append(row)


linksWithCoverage = []

wynik = []
myFile = open('results/treeWithCoverage.csv', 'w')
for x in links:
    for r in results:
        # print(r['links'])
        if r['links'][:-1] == x[0]:
            myFile = open('results/treeWithCoverage.csv', 'a+')
            with myFile:
                myFields = ['links', 'coverage']
                writer = csv.DictWriter(myFile, fieldnames=myFields)
                writer.writerow({'links': x[0], 'coverage': r['coverage']})
                linksWithCoverage.append({'links': x[0], 'coverage': r['coverage']})
# for x in results:
#     if x['net'] != 'net':
#         print(x['net'])
#         sim = simulation(x['net'])
#         myFile = open('results/resultWithE.csv', 'a+')
#         with myFile:
#             myFields = ['net', 'coverage', 'nodes', 'edges', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
#             writer = csv.DictWriter(myFile, fieldnames=myFields)
#             edges.append(sim[1])
#             writer.writerow({'net': x['net'], 'coverage': x['coverage'], 'nodes': sim[0], 'edges': sim[1], 'closeness': sim[2], 'transitivity': sim[3],
#                              'eigenvector': sim[4], 'betweenness': sim[5]})
#
check = links[0][0]
level = 0
for x in range(0, len(links)):
    # print(links[x][0][:-4])
    # print(links[x+1][0])
    if(x < len(links)-1):
        if(check[:-4] == links[x+1][0]):
            # print(links[x][0] + ' ' + str(level));
            level = level + 1
            check = links[x + 1][0]
        else:
            check = links[x+1][0]
            level = 0;

max = 0
previous = 0

print(len(links))
print(len(linksWithCoverage))

max = 0
previous = 0

for i in range(0, len(links)):
    previous = i
    # links[i][0] = str(links[i][0]) + ' G'
    max = 0
    for r in range(0, len(linksWithCoverage)):

        if(links[i][0][:-4] == linksWithCoverage[r]['links']):

            # print(links[i][0][:-6])
            # print(linksWithCoverage[r]['links'])
            # print(max)
            # print(float(linksWithCoverage[r]['coverage']))

            if max < float(linksWithCoverage[r]['coverage']):
                max = float(linksWithCoverage[r]['coverage'])
                links[r][0] = str(links[r][0]) + ' G'
                links[previous][0] = links[previous][0][:-2]
                print(links[r][0])

                previous = int(r)
            # print(results[r]['links'])

# for l in links:
    # print(l)
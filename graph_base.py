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

# print(len(links))
#print(linksWithCoverage)

max = 0
previous = 0
trash = []
tmp = []

# len = 11
maxlen = 59
pattern = ''
patArr = []

for e1 in linksWithCoverage:
    if not any(d['links'] == e1['links'] for d in patArr):
        # print('E1 ********', e1)
        pattern = e1['links']
        tmp = e1
        patArr.append(e1)
        for i in range(7, 59, 4):
            max = 0
            if len(pattern) == i:
                for e2 in linksWithCoverage:
                    if len(e2['links']) == i+4:
                        if pattern in e2['links']:
                            if(float(max) < float(e2['coverage'])):
                                # print('E2 ********', e2)
                                max = e2['coverage']
                                tmp = e2
                if not any(d['links'] == tmp['links'] for d in patArr):
                    pattern = tmp['links']
                    patArr.append(tmp)

# for p in patArr:
#     myFile = open('results/greedyTreeWithCoverage.csv', 'a+')
#     with myFile:
#         myFields = ['links', 'coverage']
#         writer = csv.DictWriter(myFile, fieldnames=myFields)
#         writer.writerow({'links': p['links'], 'coverage': p['coverage']})

maxArr = []
tmp = 0
for i in range(7, 59, 4):
    max = 0
    for e2 in linksWithCoverage:
        if len(e2['links']) == i:
            if(float(max) < float(e2['coverage'])):
                # print('E2 ********', e2)
                max = e2['coverage']
                tmp = e2
    if(tmp is not 0):
        maxArr.append(tmp)



randArr = []

for e1 in linksWithCoverage:
    if not any(d['links'] == e1['links'] for d in randArr):
        # print('E1 ********', e1)
        pattern = e1['links']
        tmp = e1
        # randArr.append(e1)
        for i in range(7, 59, 4):
            max = 0
            if len(pattern) == i:
                for e2 in linksWithCoverage:
                    if len(e2['links']) == i+4:
                        if pattern in e2['links']:
                            if(float(max) < float(e2['coverage'])):
                                if not any(d['links'] == e2['links'] for d in randArr):
                                    randArr.append(e2)
                                    pattern = e2['links']
                                    # print('E2 ********', e2)
                                    break


def searchMax(length):
    for m in maxArr:
        if (len(m['links']) == length):
            return m

# for m in randArr:
    # print('aaaaa', m)
i = int(random.uniform(0, len(linksWithCoverage)))

myFile = open('results/greedyToDisplay.csv', 'w')
myFile = open('results/maxToDisplay.csv', 'w')
myFile = open('results/randomToDisplay.csv', 'w')

for t in patArr:
    print("*****", t['links'])
    for i in range (i, len(linksWithCoverage)):
        if(len(t['links']) == 11):
            print("JEST 9", t)
        if(i == len(linksWithCoverage)-1):
            i = int(random.uniform(0,len(linksWithCoverage)))
        if (len(linksWithCoverage[i]['links']) == len(t['links'])):
            max = searchMax(len(t['links']))
            #print(t['links'], ' i ', linksWithCoverage[i]['links'], ' i ', max['links'])
            myFile = open('results/greedyToDisplay.csv', 'a+')
            with myFile:
                myFields = ['links', 'coverage']
                writer = csv.DictWriter(myFile, fieldnames=myFields)
                writer.writerow({'links': t['links'], 'coverage': t['coverage']})

            myFile = open('results/maxToDisplay.csv', 'a+')
            with myFile:
                myFields = ['links', 'coverage']
                writer = csv.DictWriter(myFile, fieldnames=myFields)
                writer.writerow({'links': max['links'], 'coverage': max['coverage']})

            myFile = open('results/randomToDisplay.csv', 'a+')
            with myFile:
                myFields = ['links', 'coverage']
                writer = csv.DictWriter(myFile, fieldnames=myFields)
                writer.writerow({'links': linksWithCoverage[i]['links'], 'coverage': linksWithCoverage[i]['coverage']})
            break


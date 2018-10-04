import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.colors
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import random

class Case:
    pp = 0
    seed = []
    coverage = 0
    net = ''


class Seed:
    seed = []

    def createSeed(self, rawList):
        self.seed = rawList.replace("[","").replace("]","").replace(",","").replace("'","").split(' ')

class Network:
    net = ''
    nodes = []
    edges = []
    closeness = 0
    transitivity = 0
    eigenvector = 0
    betweenness = 0
    coverage = 0
    listOfNetworksWithMaxCoverage = []
    listOfNetworksWithMinCoverage = []
    difference = ''


    def updateNetworkEdges(self, networkList):

        listOfReader = []

        with open('../results/graphs.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for r in reader:
                listOfReader.append(r);

        for network in networkList:
            for net in listOfReader:
                if(net != []):
                    if(network.net == net[0]):
                        print(network.edges.listOfPairs)
                        edges = Edges()
                        edges.createList(net[2][:-1])
                        network.edges = edges
                        print(network.edges.listOfPairs)


    def createRankingWithMaxCoverage(self, networkList):

        max = Network()
        max.coverage = 0

        for i in range(3, 16):
            max = Network()
            max.coverage = 0
            for network in networkList:
                if (len(network.edges.listOfPairs)) == i:
                    if (float(max.coverage) < float(network.coverage)):
                        max = network
            self.listOfNetworksWithMaxCoverage.append(max)

    def createRankingWithMinCoverage(self, networkList):

        min = Network()
        min.coverage = 10

        for i in range(3, 16):
            min = Network()
            min.coverage = 10
            for network in networkList:
                if (len(network.edges.listOfPairs)) == i:
                    if (float(min.coverage) > float(network.coverage)):
                        min = network
            self.listOfNetworksWithMinCoverage.append(min)
            # print(min)

    def createCsv(self, name, dataset):
        # print('greedy-OP/results/' + name +'.csv')

        myFields = ['net', 'coverage', 'nodes', 'edges', 'links', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
        myFile = open('greedy-OP/results/' + name + '.csv', 'w')
        with myFile:
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader();

        for data in dataset:
            # print(data)


            myFile = open('greedy-OP/results/' + name +'.csv', 'a+')
            with myFile:
                writer = csv.DictWriter(myFile, fieldnames=myFields)
                writer.writerow({'net': data.net, 'coverage': data.coverage, 'nodes': data.nodes, 'edges': data.edges.listOfPairs, 'links': len(data.edges.listOfPairs), 'closeness': data.closeness, 'transitivity': data.transitivity,
                                 'eigenvector': data.eigenvector, 'betweenness': data.betweenness})

class Edges:
    listOfPairs = []

    def createList(self, rawList):
        self.listOfPairs = rawList.split(" ")


class Greedy:

    greedy = []
    pattern = []
    number = 0
    coverage = 0
    listOfPairs = 0
    net = ''
    maximum = 0
    maximumNet = []
    maximumSeq = []
    increase = 0
    greedySeq = []
    restOfNets = []

    def createGreedySequences(self, network, networks):

        self.greedy = []
        self.greedySeq = []
        self.restOfNets = []
        self.listOfPairs = 0

        self.pattern = network
        self.coverage = network.coverage
        self.net = network.net
        self.listOfPairs = len(network.edges.listOfPairs)

        self.searchPatternInNetworksList(self.pattern, networks)
        self.greedySeq.append({'net': self.pattern, 'difference': [], 'increase': 0})
        self.greedy.append({'number': self.number, 'net': self.pattern})
        self.coverage = self.pattern.coverage

    def searchPatternInNetworksList(self, pattern, networks):

        max = pattern

        for network2 in networks:

            last = []
            print(pattern.net)
            if (network2.net[0] == pattern.net[0]):
                if (len(network2.edges.listOfPairs) - len(pattern.edges.listOfPairs) == 1):
                    if set(pattern.edges.listOfPairs).issubset(set(network2.edges.listOfPairs)):
                        if not any(d == pattern for d in self.greedy):
                            self.restOfNets.append({'number': self.number + 1, 'net': network2.net})
                            if(max.coverage < network2.coverage):
                                max = network2


        if(max.coverage != pattern.coverage):
            self.number = self.number + 1
            self.coverage = max.coverage
            # self.listOfPairs = len(max.edges.listOfPairs)

            # #print(self.number, pattern.edges.listOfPairs)
            pattern.number = self.number


            self.difference = list(set(max.edges.listOfPairs) - set(pattern.edges.listOfPairs))
            increase = float(max.coverage) - float(pattern.coverage)
            self.greedySeq.append({'net': self.pattern, 'difference': self.difference, 'increase': increase})

            self.greedy.append({'number': self.number, 'net': pattern})
            last = network2.edges.listOfPairs
            self.pattern = max




            self.searchPatternInNetworksList(self.pattern, networks)

    def createSequences(self, network, networks):

        self.greedy = []
        self.greedySeq = []
        self.restOfNets = []
        self.listOfPairs = 0

        self.pattern = network
        self.coverage = network.coverage
        self.net = network.net

        # print(network.edges.listOfPairs)
        self.listOfPairs = len(network.edges.listOfPairs)

        self.searchRandomPatternInNetworksList(self.pattern, networks)
        self.greedySeq.append({'net': self.pattern, 'difference': [], 'increase': 0})
        self.greedy.append({'number': self.number, 'net': self.pattern})
        # print('RANDOM', self.pattern.edges.listOfPairs)
        self.coverage = self.pattern.coverage


    def searchArray(self, pattern, networks):
        for network in networks:
            if(set(pattern).issubset(set(network.edges.listOfPairs))):
                print(network.net, network.edges.listOfPairs);



    def searchRandomPatternInNetworksList(self, pattern, networks):

        rand = pattern
        randomArray = []

        for network2 in networks:

            if (network2.net[0] == pattern.net[0]):
                if (len(network2.edges.listOfPairs) - len(pattern.edges.listOfPairs) == 1):
                    if set(pattern.edges.listOfPairs).issubset(set(network2.edges.listOfPairs)):
                            rand = network2
                            randomArray.append(network2)

        if (rand.coverage != pattern.coverage):
            self.number = self.number + 1
            # self.listOfPairs = len(rand.edges.listOfPairs)

            # print(self.net, self.number, pattern.edges.listOfPairs, self.coverage)
            pattern.number = self.number

            self.difference = list(set(rand.edges.listOfPairs) - set(pattern.edges.listOfPairs))
            increase = float(rand.coverage) - float(pattern.coverage)
            self.greedySeq.append({'net': self.pattern, 'difference': self.difference, 'increase': increase})

            # print('RANDOM', self.pattern.edges.listOfPairs)

            self.greedy.append({'number': self.number, 'net': self.pattern})
            last = network2.edges.listOfPairs

            i = random.randint(0, len(randomArray)-1)
            # print(i)
            # print(int(i))
            # print(randomArray)
            # if(self.pattern.net == '43.txt'):
            for r in randomArray:
                # print(r.net)
                self.restOfNets.append({'number': self.number, 'net': r.net})

            if(len(randomArray) != 0):
                self.pattern = randomArray[int(i)]
                self.coverage = pattern.coverage

            else:
                self.pattern = rand
                self.coverage = rand.coverage

            # print(self.net, self.number, pattern.edges.listOfPairs, self.coverage)
            self.searchRandomPatternInNetworksList(self.pattern, networks)

    def createAllSequences(self, network, networks):

        self.greedy = []

        self.pattern = network
        self.coverage = network.coverage
        self.net = network.net

        self.listOfPairs = len(network.edges.listOfPairs)
        self.greedy.append({'number': self.number, 'net': self.pattern, 'coverage': self.pattern.coverage})
        self.searchAllPatternInNetworksList(self.pattern, networks)

    def searchAllPatternInNetworksList(self, pattern, networks):

        rand = pattern
        randomArray = []
        # print('MAXIMA', self.net, self.number, pattern.edges.listOfPairs, self.coverage)

        for network2 in networks:
            if (network2.net[0] == pattern.net[0]):
                if (len(network2.edges.listOfPairs) - len(pattern.edges.listOfPairs) == 1):
                    if set(pattern.edges.listOfPairs).issubset(set(network2.edges.listOfPairs)):
                        rand = network2
                        randomArray.append(network2)
                        self.greedy.append({'number': self.number, 'net': rand, 'coverage': rand.coverage})
        # print('MAXIMA', pattern.net, pattern.number, pattern.edges.listOfPairs, pattern.coverage)
        # self.greedy.append({'number': self.number, 'net': rand, 'coverage': rand.coverage})
        if (rand.net != pattern.net):
            # if self.net == '42.txt':
            #     print(pattern.net, pattern.edges.listOfPairs)
            self.number = self.number + 1
            self.coverage = rand.coverage
            self.listOfPairs = len(rand.edges.listOfPairs)

            # #print('MAXIMA', rand.net, self.number, rand.edges.listOfPairs, self.coverage)
            # pattern.number = self.number
            self.greedy.append({'number': self.number, 'net': rand, 'coverage': rand.coverage})
            # #print("GREEDYY ARRAY", self.greedy)
            last = network2.edges.listOfPairs

            # i = random.uniform(0, len(randomArray))
            # #print(int(i))
            # #print(randomArray)

            for r in randomArray:
                self.searchAllPatternInNetworksList(r, networks)


    def searchInGreedyMaximum(self):
        self.maximum = 0
        tmpMaximum = []
        for g in self.greedy:
            # if self.net == '42.txt':
                # print(g['net'].net, g['net'].edges.listOfPairs)
            if(self.maximum < float(g['net'].coverage)):
                self.maximum = float(g['net'].coverage)
                self.maximumNet = g['net']
        if(self.maximum != 0):
            self.maximumSeq = []
            self.maximumSeq.append({'net': self.maximumNet, 'difference': [], 'increase': 0})

            self.createMaximumSequences(self.maximumNet)
        if(self.maximum == 0):
            self.maximum = self.coverage



    def createMaximumSequences(self, pattern):
        for g in self.greedy:
            if(len(pattern.edges.listOfPairs) - len(g['net'].edges.listOfPairs) == 1):
                if set(g['net'].edges.listOfPairs).issubset(set(pattern.edges.listOfPairs)):
                    self.difference = list(set(pattern.edges.listOfPairs) - set(g['net'].edges.listOfPairs))
                    increase = float(pattern.coverage) - float(g['net'].coverage)
                    self.maximumSeq.append({'net': g['net'], 'difference': self.difference, 'increase': increase})
                    self.createMaximumSequences(g['net'])
                    break;
        # if (last != []):
        #     self.greedy.append(last)



    def createCsv(self, name, dataset):
        # print('greedy-OP/results/' + name +'.csv')

        myFields = ['number', 'net', 'coverage', 'nodes', 'edges', 'links', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
        myFile = open('greedy-OP/results/' + name + '.csv', 'w')
        with myFile:
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader();

        for dataset in dataset:
            for data in dataset.greedy:
                myFile = open('greedy-OP/results/' + name +'.csv', 'a+')
                with myFile:
                    writer = csv.DictWriter(myFile, fieldnames=myFields)
                    writer.writerow({'number': data['number'], 'net': data['net'].net, 'coverage': data['net'].coverage, 'nodes': data['net'].nodes, 'edges': data['net'].edges.listOfPairs, 'links': len(data['net'].edges.listOfPairs), 'closeness': data['net'].closeness, 'transitivity': data['net'].transitivity,
                                     'eigenvector': data['net'].eigenvector, 'betweenness': data['net'].betweenness})

    def createDifferenceCsv(self, name, dataset):
        # print('greedy-OP/results/' + name +'.csv')

        myFields = ['net', 'coverage', 'edges', 'closeness', 'transitivity', 'eigenvector', 'betweenness', 'rest']
        myFile = open(name + '.csv', 'w')
        with myFile:
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writeheader();

        for data in dataset:
            # print(data)
            myFile = open(name +'.csv', 'a+')
            with myFile:
                writer = csv.DictWriter(myFile, fieldnames=myFields)
                writer.writerow({'net': data['net'], 'coverage': data['coverage'], 'edges': data['edges'],
                                 'closeness': data['closeness'], 'transitivity': data['transitivity'],'eigenvector': data['eigenvector'], 'betweenness': data['betweenness']})

    def createTable1(self, name, dataset):
        # print('greedy-OP/results/' + name +'.csv')


        myFields = ['links', 'net', 'space','0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', 'coverage']
        myFile = open(name + '.csv', 'w')

        for data in dataset:
            # revertDataset = sot
            # for i, x in enumerate(data.maximumSeq):
            row = {'links': data.listOfPairs, 'net': data.net, 'space': ' ', 'coverage': data.coverage}
            # x = {str(i):x['net'].coverage for i, x in enumerate(reversed(data.maximumSeq))} ### UWAŻAC NA TOOOOO KONIECZNIE
            x = {str(i):x['net'].coverage for i, x in enumerate(data.greedy)} ### UWAŻAC NA TOOOOO KONIECZNIE
            row.update(x)

            # print(row)

            myFile = open(name + '.csv', 'a+')
            with myFile:
                # myFields = [i for i, x in enumerate(data.greedy)]
                writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
                writer.writerow(row)

                # writer.writerow({i:x['net'].coverage for i, x in enumerate(data.greedy)})
        # print('\n')


listOfNetworks = []
allCases = []

# with open('../results/results.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for row in reader:
#         tmpCase = Case()
#         if row != []:
#             if row[0] != 'pp':
#                 tmpCase.pp = float(row[0])
#                 tmpCase.coverage = row[2]
#                 tmpCase.net = row[3]
#
#                 seed = Seed()
#                 seed.createSeed(row[1])
#                 tmpCase.seed = seed.seed
#
#                 allCases.append(tmpCase)


with open('../results/resultWithE.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        tmpNetwors = Network()
        if row != []:
            tmpNetwors.net = row[0]
            tmpNetwors.coverage = row[1]
            tmpNetwors.betweenness = row[7]
            tmpNetwors.closeness = row[4]
            tmpNetwors.nodes = row[2]
            tmpNetwors.eigenvector = row[6]
            tmpNetwors.transitivity = row[5]
            tmpNetwors.number = 0

            edges = Edges()
            edges.createList(row[3][:-1])
            tmpNetwors.edges = edges

            listOfNetworks.append(tmpNetwors)


tmpNetwors.updateNetworkEdges(listOfNetworks)

listOfGreedy = []
listOfRandom = []
listOfMaximum = []


for l in listOfNetworks:
    print(l.net)
    maximum = Greedy()
    maximum.createAllSequences(l, listOfNetworks)
    maximum.searchInGreedyMaximum()
    listOfMaximum.append(maximum)
    for m in maximum.maximumSeq:
        print(m['net'].net, m['net'].coverage)
    print('\n')
    print('\n')

for l in listOfNetworks:
    greedy = Greedy()
    greedy.createGreedySequences(l, listOfNetworks)
    listOfGreedy.append(greedy)

for l in listOfNetworks:
    rand = Greedy()
    rand.createSequences(l, listOfNetworks)
    listOfRandom.append(rand)

for i in range(len(listOfGreedy)):

    # print(listOfMaximum[i].maximum)
    print(listOfRandom[i].coverage)
    print(listOfGreedy[i].coverage)
    print('\n')

    print(listOfMaximum[i].net, listOfMaximum[i].coverage)
    for m in reversed(listOfMaximum[i].maximumSeq):
        print(m['net'].net, m['net'].edges.listOfPairs, m['net'].coverage)
    print('\n')
    print('RANDOM')
    print(listOfRandom[i].net, listOfRandom[i].coverage)
    for m in listOfRandom[i].greedySeq:
        print(m['net'].net, m['net'].edges.listOfPairs, m['net'].coverage, listOfRandom[i].restOfNets)
    print('\n')
    print('GREEDY')
    print(listOfGreedy[i].net, listOfGreedy[i].coverage)
    for m in listOfGreedy[i].greedySeq:
        print(m['net'].net, m['net'].edges.listOfPairs, m['net'].coverage, listOfGreedy[i].restOfNets)
    print('\n')

listOfDifferencesInMax = []
listOfDifferencesInGreedy = []
listOfDifferencesInRandom = []

for m in listOfMaximum:
    for s in m.maximumSeq:
       listOfDifferencesInMax.append({'net': s['net'].net, 'coverage': s['net'].coverage, 'edges': s['net'].edges.listOfPairs, 'difference': s['difference'], 'increase':  s['increase'],
                                      'closeness': s['net'].closeness, 'transitivity': s['net'].transitivity, 'eigenvector': s['net'].eigenvector, 'betweenness': s['net'].betweenness})

for g in listOfGreedy:
    for s in g.greedySeq:
        listOfDifferencesInGreedy.append(
            {'net': s['net'].net, 'coverage': s['net'].coverage, 'edges': s['net'].edges.listOfPairs,
             'closeness': s['net'].closeness, 'transitivity': s['net'].transitivity,
             'eigenvector': s['net'].eigenvector, 'betweenness': s['net'].betweenness, 'rest': g.restOfNets})


# greedy.createTable1('random', listOfRandom)
# greedy.createTable1('greedy', listOfGreedy)
# greedy.createTable1('max', listOfMaximum)

for g in listOfRandom:
        for s in g.greedy:
            print(s['net'].coverage)
            listOfDifferencesInRandom.append(
                {'net': s['net'].net, 'coverage': s['net'].coverage, 'edges': s['net'].edges.listOfPairs,
                 'closeness': s['net'].closeness, 'transitivity': s['net'].transitivity,
                 'eigenvector': s['net'].eigenvector, 'betweenness': s['net'].betweenness, 'rest': g.restOfNets})


greedy.createTable1('random', listOfRandom)
# greedy.createTable1('max', listOfMaximum)
greedy.createTable1('greedy', listOfGreedy)

# greedy.createDifferenceCsv('listOfDifferencesInMaximum', listOfDifferencesInMax)
# greedy.createDifferenceCsv('listOfDifferencesInRandom', listOfDifferencesInRandom)
# greedy.createDifferenceCsv('listOfDifferencesInGreedy', listOfDifferencesInGreedy)






# greedyToDisplay = []
# greedyToDisplayAll = []
#
# greedy = []
# rand = []
# max = []
# maxNet = ''

#
# for l in listOfMaximum:
#     if (len(l.maximumSeq) == 6):
#         for m in l.maximumSeq:
#             maxNet = l.net
#             print("MAXIMUM", m['net'].edges.listOfPairs, m['difference'])
#             max.append(m['net'])
#     if (len(l.maximumSeq) == 6):
#         break
#
# for l in listOfGreedy:
#     if (l.net == maxNet):
#         for g in l.greedy:
#             print("GREEDY", g['number'], g['net'].edges.listOfPairs)
#             greedy.append(g['net'])
#     if (l.net == maxNet):
#         break
#
#
# for l in listOfRandom:
#     if (l.net == maxNet):
#         for g in l.greedy:
#             # print("RANDOM", g['number'], g['net'].edges.listOfPairs)
#             rand.append(g['net'])
#     if (len(l.greedy) == maxNet):
#         break
#
#
# networks = Network()
# networks.createRankingWithMaxCoverage(listOfNetworks)

# greedy = Greedy()

# plotArray = []
#
# listOfNetworksSorted = sorted(listOfNetworks, key=lambda x: x.coverage, reverse=True)
#
#
# x = []
# y = []
# col = []
# alp = []
# ylines = []
# xNodes = []
# networks.createRankingWithMinCoverage(listOfNetworks)

# for net in networks.listOfNetworksWithMinCoverage:
#     ylines.append(float(net.coverage))
#     # print(net.edges.listOfPairs)
#
# for n in listOfNetworksSorted:
#     for m in max:
#         print(m)
#         if(m.coverage == n.coverage):
#             col.append('C3')
#             print(n.coverage)
#             y.append(float(n.coverage))
#             xNodes.append(float(len(n.edges.listOfPairs)))
#             break
#     for g in greedy:
#         if(g.coverage == n.coverage):
#             col.append('C1')
#             y.append(float(n.coverage))
#             xNodes.append(float(len(n.edges.listOfPairs)))
#             break
#     for r in rand:
#         if (r.coverage == n.coverage):
#             col.append('C7')
#             y.append(float(n.coverage))
#             xNodes.append(float(len(n.edges.listOfPairs)))
#             break
#     # if (g.coverage != n.coverage != m.coverage):
#     #     y.append(float(n.coverage))
#     #     col.append('C0')
#     #     xNodes.append(float(len(n.edges.listOfPairs)))
#
#
# x = range(len(y))
# x = sorted(x, reverse=True)

# ########### FIGURE 1 ###################
#
#
# fig = plt.figure(figsize=(10,10))
# ax = fig.add_subplot(111)
#
# # ax.plot([1, 2, 3, 4, 10], [10, 20, 25, 30, 100], color='lightblue', linewidth=3)
# # ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
#
# # ax.scatter(xNodes, y, color=col, s=10, label=col)
#
# ax.scatter(x, y, color=col, s=15)
# ax.scatter([], [], color='C7', s=15)
# ax.scatter([], [], color='C1', s=15)
# # ax.scatter(y, xNodes, color=col, s=10, label=col)
#
# # ax.plot([1,150],[ylines,ylines], 'C3', lw=1)
#
# # ax.set_yscale('log')
# ax.tick_params(axis='both', which='major', labelsize=10)
# # ax.set_xlim(0, 150)
#
# ax.legend(['MAX', 'RANDOM', 'GREEDY'])
#
# # plt.show()
# #
# fig.savefig("1GREEDYx1RANDOMx1MAX_the_same_net.png", dpi = (200))
#
#
#
# ########### FIGURE 2 ###################
#
# # y = []
# #
# # for g in listOfGreedy:
# #     for r in listOfRandom:
# #         if(float(g.coverage) != float(r.coverage)):
# #             if(g.net == r.net):
# #                 # print("ROZNICA", float(g.coverage) / float(r.coverage))
# #                 y.append(float(g.coverage) / float(r.coverage))
# #                 if float(g.coverage) / float(r.coverage) > 1.5:
# #                     for test in g.greedy:
# #                         print(test['net'].edges.listOfPairs,  " ")
# # fig = plt.figure(figsize=(10,10))
# # ax = fig.add_subplot(111)
# #
# # y = sorted(y, reverse=True)
# #
# # x = range(len(y))
# #
# # less_than_one = list(filter(lambda x: x < 1, y))
# # bigger_than_one = list(filter(lambda x: x > 1, y))
# #
# # print('LEEESSSS', len(less_than_one))
# # print('BIGGGGER', len(bigger_than_one))
# #
# # ax.scatter(x, y, color='C0', s=2, label=col)
# # ax.plot([1,128],[1,1], 'C3', lw=1)
# #
# # # ax.set_yscale('log')
# #
# #
# # ax.tick_params(axis='both', which='major', labelsize=10)
# #
# # plt.show()
# #
# # fig.savefig("coverage_ratio.png", dpi = (200))
# # fig.savefig("ratio_coverage_g.png", dpi = (200))
#
# ########### FIGURE 3 ###################
#
# listOfMaximum = []
#
# print(listOfNetworks)
# for l in listOfNetworks:
#     maximum = Greedy()
#     maximum.createAllSequences(l, listOfNetworks)
#     maximum.searchInGreedyMaximum()
#     listOfMaximum.append(maximum)
#
# for m in listOfMaximum:
#     for s in m.maximumSeq:
#         print(s['net'].net, s['net'].coverage, s['difference'], s['increase'])
#
#
# y1 = []
# y2 = []
# y3 = []
# y4 = []
# x = []
#
#
# listOfGreedy = sorted(listOfGreedy, key=lambda x: x.coverage)
# wastedNets = []
# networks = []
#
# for i in range(0, len(listOfGreedy)):
#
#     if len(listOfGreedy[i].greedy) >= 0:
#         # print("GREEDY", listOfGreedy[i].net, listOfGreedy[i].coverage)
#         y1.append(float(listOfGreedy[i].coverage))
#         networks.append(listOfGreedy[i].net)
#         for n in listOfRandom:
#             if(n.net == listOfGreedy[i].net):
#                 print("RANDOM", n.net, n.coverage)
#                 # print(m)
#                 y2.append(float(n.coverage))
#                 break
#
#
#         for m in listOfMaximum:
#             if(m.net == listOfGreedy[i].net):
#                 print("MAXIMUM", m.net, m.maximum, '\n')
#                 # print(m)
#                 y3.append(float(m.maximum))
#                 break
#
# # fig = plt.figure(figsize=(10,10))
# # ax = fig.add_subplot(111)
#
# # print(y1)
# # print(y2)
# # print(y3)
#
# # y1 = sorted(y1)
# # y2 = sorted(y2)
# # y3 = sorted(y3)
#
#
#
# x = range(len(y1))
#
# # less_than_one = list(filter(lambda x: x < 1, y))
# # bigger_than_one = list(filter(lambda x: x > 1, y))
#
# # print('LEEESSSS', len(less_than_one))
# # print('BIGGGGER', len(bigger_than_one))
#
# # ax.scatter(x, y1, color='C2', s=6, label=col)
# # ax.scatter(x, y2, color='C0', s=3, label=col)
# # ax.scatter(x, y3, color='C3', s=3, label=col)
# #
#
#
# # ax.scatter(x, y4, color='C6', s=4, label=col)
#
# # ax.set_yscale('log')
#
# #
# ax.tick_params(axis='both', which='major', labelsize=10)
#
#
# y1 = []
# y2 = []
# y3 = []
# y4 = []
# x = []
#
#
# listOfGreedy = sorted(listOfGreedy, key=lambda x: x.coverage)
# wastedNets = []
# networks = []
#
# for i in range(0, len(listOfGreedy)):
#
#     if len(listOfGreedy[i].greedy) >= 0:
#         print("GREEDY", listOfGreedy[i].net, listOfGreedy[i].coverage)
#         y1.append(float(listOfGreedy[i].coverage))
#         networks.append(listOfGreedy[i].net)
#         for n in listOfRandom:
#             if(n.net == listOfGreedy[i].net):
#                 # print("RANDOM", n.net, n.coverage)
#                 # print(m)
#                 y2.append(float(n.coverage))
#                 break
#
#
#         for m in listOfMaximum:
#             if(m.net == listOfGreedy[i].net):
#                 print("MAXIMUM", m.net, m.maximum, '\n')
#                 # print(m)
#                 y3.append(float(m.maximum))
#                 break
#
# fig = plt.figure(figsize=(10,10))
# ax = fig.add_subplot(111)
#
# print(y1)
# print(y2)
# print(y3)
#
# y1 = sorted(y1)
# y2 = sorted(y2)
# y3 = sorted(y3)
#
#
#
# x = range(len(y1))
#
# less_than_one = list(filter(lambda x: x < 1, y))
# bigger_than_one = list(filter(lambda x: x > 1, y))
#
# print('LEEESSSS', len(less_than_one))
# print('BIGGGGER', len(bigger_than_one))
#
# ax.scatter(x, y1, color='C2', s=14, label='GREEDY')
# ax.scatter(x, y2, color='C0', s=4, label='RANDOM')
# ax.scatter(x, y3, color='C3', s=4, label='MAXIMUM')
#
#
# ax.legend()
# ax.set_ylabel('COVERAGE')
# ax.set_xlabel('NETWORKS')
#
#
#
# # ax.scatter(x, y4, color='C6', s=4, label=col)
#
# # ax.set_yscale('log')
#
#
# ax.tick_params(axis='both', which='major', labelsize=10)
#
# plt.xticks(rotation='vertical')
#
# plt.show()
#
# fig.savefig("coverageXcases.png", dpi = (200))
# # plt.xticks(rotation='vertical')
#
# plt.show()
#
# fig.savefig('coverageXcases.png')
# # plt.savefig("test.png", dpi = (200))
#
#
#
# ##################### FIGURE 4 #####################
#
# # listOfRandom = sorted(listOfRandom, key=lambda x: x.coverage)
# #
# # y1 = []
# # y2 = []
# #
# # for r in listOfRandom:
# #     for g in listOfGreedy:
# #         if(r.net == g.net):
# #             y1.append(float(r.coverage))
# #             y2.append(float(g.coverage))
#
# # for case in allCases:
# #     for g in listOfGreedy:
# #         if(case.net == g.net):
# #             if(len(case.seed) == 4 and case.pp == 0.5):
# #             print(len(case.seed))
#                 # y.append(float(case.coverage))
# #
# # fig = plt.figure(figsize=(10,10))
# # ax = fig.add_subplot(111)
# #
# #
# #
# # x = range(len(y1))
# #
# # print(len(x))
# #
# #
# # ax.scatter(x, y1, color='C2', s=4, label='RANDOM')
# # ax.scatter(x, y2, color='C0', s=4, label='GREEDY')
# # # ax.scatter(x, y3, color='C3', s=4, label=col)
# #
# # # plt.show()
# # ax.legend()
# # ax.set_ylabel('COVERAGE')
# # ax.set_xlabel('CASES')
# #
# # fig.savefig("test.png", dpi = (200))

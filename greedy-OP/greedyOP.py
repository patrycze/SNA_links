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
        print('greedy-OP/results/' + name +'.csv')

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

    def createGreedySequences(self, network, networks):

        self.greedy = []

        self.pattern = network
        self.coverage = network.coverage
        self.net = network.net
        self.listOfPairs = len(network.edges.listOfPairs)
        self.searchPatternInNetworksList(self.pattern, networks)

    def searchPatternInNetworksList(self, pattern, networks):

        max = pattern

        for network2 in networks:

            last = []

            if (len(network2.edges.listOfPairs) - len(pattern.edges.listOfPairs) == 1):
                if set(pattern.edges.listOfPairs).issubset(set(network2.edges.listOfPairs)):
                    if not any(d == pattern for d in self.greedy):

                        if(max.coverage < network2.coverage):
                            max = network2


        if(max.coverage != pattern.coverage):
            self.number = self.number + 1
            self.coverage = max.coverage
            self.listOfPairs = len(max.edges.listOfPairs)

            # print(self.net, self.number, max.edges.listOfPairs, self.coverage)
            pattern.number = self.number
            self.greedy.append({'number': self.number, 'net': pattern})
            last = network2.edges.listOfPairs
            self.pattern = max

            self.searchPatternInNetworksList(self.pattern, networks)

    def createSequences(self, network, networks):

        self.greedy = []

        self.pattern = network
        self.coverage = network.coverage
        self.net = network.net

        self.listOfPairs = len(network.edges.listOfPairs)

        self.searchRandomPatternInNetworksList(self.pattern, networks)

    def searchRandomPatternInNetworksList(self, pattern, networks):

        rand = pattern
        randomArray = []

        for network2 in networks:


            if (len(network2.edges.listOfPairs) - len(pattern.edges.listOfPairs) == 1):
                if set(pattern.edges.listOfPairs).issubset(set(network2.edges.listOfPairs)):
                        rand = network2
                        randomArray.append(network2)

        if (rand.coverage != pattern.coverage):
            self.number = self.number + 1
            self.listOfPairs = len(rand.edges.listOfPairs)

            # print(self.net, self.number, pattern.edges.listOfPairs, self.coverage)
            pattern.number = self.number
            self.greedy.append({'number': self.number, 'net': pattern})
            last = network2.edges.listOfPairs

            i = random.uniform(0, len(randomArray))
            # print(int(i))
            # print(randomArray)

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

        self.searchAllPatternInNetworksList(self.pattern, networks)

    def searchAllPatternInNetworksList(self, pattern, networks):

        rand = pattern
        randomArray = []
        # print('MAXIMA', self.net, self.number, pattern.edges.listOfPairs, self.coverage)

        for network2 in networks:

            if (len(network2.edges.listOfPairs) - len(pattern.edges.listOfPairs) == 1):
                if set(pattern.edges.listOfPairs).issubset(set(network2.edges.listOfPairs)):
                    rand = network2
                    randomArray.append(network2)

        # print('MAXIMA', pattern.net, pattern.number, pattern.edges.listOfPairs, pattern.coverage)
        self.greedy.append({'number': self.number, 'net': rand, 'coverage': rand.coverage})
        if (rand.net != pattern.net):
            self.number = self.number + 1
            self.coverage = rand.coverage
            self.listOfPairs = len(rand.edges.listOfPairs)

            print('MAXIMA', rand.net, self.number, rand.edges.listOfPairs, self.coverage)
            # pattern.number = self.number
            self.greedy.append({'number': self.number, 'net': rand, 'coverage': rand.coverage})
            # print("GREEDYY ARRAY", self.greedy)
            last = network2.edges.listOfPairs

            # i = random.uniform(0, len(randomArray))
            # print(int(i))
            # print(randomArray)

            for r in randomArray:
                self.searchAllPatternInNetworksList(r, networks)


    def searchInGreedyMaximum(self):
        self.maximum = 0
        for g in self.greedy:
            print('MAX', g['coverage'])
            if(self.maximum < float(g['coverage'])):
                self.maximum = float(g['coverage'])
        print('MAX????', self.net, self.maximum)
        if(self.maximum == 0):
            self.maximum = self.coverage


        # if (last != []):
        #     self.greedy.append(last)
    def createCsv(self, name, dataset):
        print('greedy-OP/results/' + name +'.csv')

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


listOfNetworks = []
allCases = []

with open('C:/Users/Patryk/Desktop/SNA_Links/SNA_links/results/results.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        tmpCase = Case()
        if row != []:
            if row[0] != 'pp':
                tmpCase.pp = float(row[0])
                tmpCase.coverage = row[2]
                tmpCase.net = row[3]

                seed = Seed()
                seed.createSeed(row[1])
                tmpCase.seed = seed.seed

                allCases.append(tmpCase)


with open('C:/Users/Patryk/Desktop/SNA_Links/SNA_links/results/resultWithE.csv', 'r') as csvfile:
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

listOfGreedy = []
listOfRandom = []


for l in listOfNetworks:
    greedy = Greedy()
    greedy.createGreedySequences(l, listOfNetworks)
    listOfGreedy.append(greedy)
    # print(greedy)

for l in listOfNetworks:
    rand = Greedy()
    rand.createSequences(l, listOfNetworks)
    listOfRandom.append(rand)
    # print(greedy)

greedyToDisplay = []
greedyToDisplayAll = []
greedy = []
rand = []

for l in listOfGreedy:
    for g in l.greedy:
        if(len(l.greedy) == 6):
            # print("GREEDY", g['number'], g['net'].edges.listOfPairs)
            greedy.append(g['net'])
    if (len(l.greedy) == 6):
        break

for l in listOfRandom:
    for g in l.greedy:
        if(len(l.greedy) == 6):
            # print("RANDOM", g['number'], g['net'].edges.listOfPairs)
            rand.append(g['net'])
    if (len(l.greedy) == 6):
        break


networks = Network()
networks.createRankingWithMaxCoverage(listOfNetworks)

# greedy = Greedy()

plotArray = []

listOfNetworksSorted = sorted(listOfNetworks, key=lambda x: x.coverage, reverse=True)


x = []
y = []
col = []
alp = []
ylines = []
xNodes = []
networks.createRankingWithMinCoverage(listOfNetworks)

for net in networks.listOfNetworksWithMinCoverage:
    ylines.append(float(net.coverage))
    # print(net.edges.listOfPairs)

for n in listOfNetworksSorted:
    for m in networks.listOfNetworksWithMaxCoverage:
        if(m.coverage == n.coverage):
            col.append('C3')
            y.append(float(n.coverage))
            xNodes.append(float(len(n.edges.listOfPairs)))
            break
    for g in greedy:
        if(g.coverage == n.coverage):
            col.append('C1')
            y.append(float(n.coverage))
            xNodes.append(float(len(n.edges.listOfPairs)))
            break
    for r in rand:
        if (r.coverage == n.coverage):
            col.append('C7')
            y.append(float(n.coverage))
            xNodes.append(float(len(n.edges.listOfPairs)))
            break
    if (g.coverage != n.coverage != m.coverage):
        y.append(float(n.coverage))
        col.append('C0')
        xNodes.append(float(len(n.edges.listOfPairs)))
        # col.append([0,126,158])

# print(y[10:30])


alphas = np.linspace(0.1, 1, 10)
rgba_colors = np.zeros((10,4))
# for red the first column needs to be one
rgba_colors[:,0] = 1.0
# the fourth column needs to be your alphas
rgba_colors[:, 3] = alphas


x = range(len(y))
x = sorted(x, reverse=True)

########### FIGURE 1 ###################
#
# plt.subplot(212)
#
# fig = plt.figure(figsize=(10,10))
# ax = fig.add_subplot(111)
#
# # ax.plot([1, 2, 3, 4, 10], [10, 20, 25, 30, 100], color='lightblue', linewidth=3)
# # ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
#
# # ax.scatter(xNodes, y, color=col, s=10, label=col)
#
# ax.scatter(x, y, color=col, s=10, label=col)
# # ax.scatter(y, xNodes, color=col, s=10, label=col)
#
# ax.plot([1,150],[ylines,ylines], 'C3', lw=1)
#
# # ax.set_yscale('log')
# ax.tick_params(axis='both', which='major', labelsize=10)
# # ax.set_xlim(0, 150)
#
# plt.show()
#
# fig.savefig("test.png", dpi = (200))

########## FIGURE 2 ###################
#
# y = []
#
# for g in listOfGreedy:
#     for r in listOfRandom:
#         if(float(g.coverage) != float(r.coverage)):
#             if(g.net == r.net):
#                 # print("ROZNICA", float(g.coverage) / float(r.coverage))
#                 y.append(float(g.coverage) / float(r.coverage))
#                 if float(g.coverage) / float(r.coverage) > 1.5:
#                     for test in g.greedy:
#                         print(test['net'].edges.listOfPairs,  " ")
# fig = plt.figure(figsize=(10,10))
# ax = fig.add_subplot(111)
#
# y = sorted(y, reverse=True)
#
# x = range(len(y))
#
# less_than_one = list(filter(lambda x: x < 1, y))
# bigger_than_one = list(filter(lambda x: x > 1, y))
#
# print('LEEESSSS', len(less_than_one))
# print('BIGGGGER', len(bigger_than_one))
#
# ax.scatter(x, y, color='C0', s=2, label=col)
# ax.plot([1,128],[1,1], 'C3', lw=1)
#
# # ax.set_yscale('log')
#
#
# ax.tick_params(axis='both', which='major', labelsize=10)
#
# plt.show()
#
# fig.savefig("ratio_coverage_g.png", dpi = (200))

########## FIGURE 3 ###################

listOfMaximum = []

print(listOfNetworks)
for l in listOfNetworks:
    maximum = Greedy()
    maximum.createAllSequences(l, listOfNetworks)
    maximum.searchInGreedyMaximum()
    # print("MAXIMUM", maximum.net, maximum.maximum)
    listOfMaximum.append(maximum)



y1 = []
y2 = []
y3 = []
y4 = []
x = []


listOfGreedy = sorted(listOfGreedy, key=lambda x: x.coverage)
wastedNets = []
networks = []

for i in range(0, len(listOfGreedy)):

    if len(listOfGreedy[i].greedy) >= 0:
        print("GREEDY", listOfGreedy[i].net, listOfGreedy[i].coverage)
        y1.append(float(listOfGreedy[i].coverage))
        networks.append(listOfGreedy[i].net)
        for n in listOfRandom:
            if(n.net == listOfGreedy[i].net):
                # print("RANDOM", n.net, n.coverage)
                # print(m)
                y2.append(float(n.coverage))
                break


        for m in listOfMaximum:
            if(m.net == listOfGreedy[i].net):
                print("MAXIMUM", m.net, m.maximum, '\n')
                # print(m)
                y3.append(float(m.maximum))
                break

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)

# print(y1)
# print(y2)
# print(y3)

# y1 = sorted(y1)
# y2 = sorted(y2)
# y3 = sorted(y3)



x = range(len(y1))

# less_than_one = list(filter(lambda x: x < 1, y))
# bigger_than_one = list(filter(lambda x: x > 1, y))

# print('LEEESSSS', len(less_than_one))
# print('BIGGGGER', len(bigger_than_one))

ax.scatter(x, y1, color='C2', s=14, label='GREEDY')
ax.scatter(x, y2, color='C0', s=4, label='RANDOM')
ax.scatter(x, y3, color='C3', s=4, label='MAXIMUM')


ax.legend()
ax.set_ylabel('COVERAGE')
ax.set_xlabel('NETWORKS')



# ax.scatter(x, y4, color='C6', s=4, label=col)

# ax.set_yscale('log')

#
ax.tick_params(axis='both', which='major', labelsize=10)

# plt.xticks(rotation='vertical')

plt.show()

fig.savefig("coverageXcases.png", dpi = (200))
#


##################### FIGURE 4 #####################

listOfRandom = sorted(listOfRandom, key=lambda x: x.coverage)

y1 = []
y2 = []

for r in listOfRandom:
    for g in listOfGreedy:
        if(r.net == g.net):
            y1.append(float(r.coverage))
            y2.append(float(g.coverage))

# for case in allCases:
#     for g in listOfGreedy:
#         if(case.net == g.net):
#             if(len(case.seed) == 4 and case.pp == 0.5):
#             print(len(case.seed))
                # y.append(float(case.coverage))

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)



x = range(len(y1))

print(len(x))


ax.scatter(x, y1, color='C2', s=4, label='RANDOM')
ax.scatter(x, y2, color='C0', s=4, label='GREEDY')
# ax.scatter(x, y3, color='C3', s=4, label=col)

# plt.show()
ax.legend()
ax.set_ylabel('COVERAGE')
ax.set_xlabel('CASES')

fig.savefig("test.png", dpi = (200))

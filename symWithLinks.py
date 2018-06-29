from igraph import *
import random
import csv
import time


def createRanking(array):
    arr = []
    sum = 0
    for i in array:
        sum = float(i[1]) + sum
        arr.append({'index': i[0], 'value': sum})

    return arr

def readPrefixes(file, array):
    with open(file, "r") as ins:
        for line in ins:
            array.append(line.replace('\n', ''))

def readFileToArray(file, array):
    with open(file, "r") as ins:
        for line in ins:
            array.append(line.replace('\n', '').split(' '))

def searchInArray(a, b, array):
    for i in range(len(array)):
        if(array[i][0] == str(a)):
            if(array[i][0] == str(a) and array[i][1] == str(b)):
                return array[i][2]
        if (array[i][1] == str(a)):
            if(array[i][1] == str(a) and array[i][0] == str(b)):
                return array[i][3]

def searchInRanking(array, index):
    for i in range(len(array)):
        if(i == index):
            return array[i][0]

def searchInRankingScope(array, value):
    for i in array:
        if(value <= i['value']):
            return i['index']


def simulation(pp, percentage, net, ranking, run, percentageLinks, linkRanking1, linkRanking2, v, per):

    #### READ FILES WITH RANKING ####

    degreeRanking = []
    betweennessRanking = []
    eigenvectorRanking = []
    randomRanking = []

    readFileToArray('syntetic/benchmark001/rankings/' + net + '_ranking_dg.txt', degreeRanking)
    readFileToArray('syntetic/benchmark001/rankings/' + net + '_ranking_bt.txt', betweennessRanking)
    readFileToArray('syntetic/benchmark001/rankings/' + net + '_ranking_ev.txt', eigenvectorRanking)
    readFileToArray('syntetic/benchmark001/rankings/' + net + '_ranking_rn.txt', randomRanking)

    writeInfectionsToFile = open('syntetic/benchmark001/INFECTIONS/' + net[0:3] + 'infections.csv', 'a')

    degreeScope = createRanking(degreeRanking)
    betweennessScope = createRanking(betweennessRanking)
    eigenvectorScope = createRanking(eigenvectorRanking)
    randomScope = createRanking(randomRanking)

    array = []

    readFileToArray('syntetic/benchmark001/weights/' + net + '_' + str(v) + '.txt', array)

    s = 1;
    isInfecting = True

    g = Graph.Read_Ncol('syntetic/benchmark001/' + net + '.txt', directed=True)


    nodes  = Graph.vcount(g)
    g.vs["label"] = g.vs["name"]
    numberofseeds = int(round(nodes * percentage, ndigits=0))
    numberoflinks = int(round(nodes * percentageLinks, ndigits=0))
    infections = 0

    for i in range(0,nodes):
        g.vs[i]["infected"] = 0
        g.vs[i]["used"] = 0

    #print('LICZBA SEEDOW', numberofseeds)
    for seeds in range(0, numberofseeds):

        #x = g.vs.find(str(seeds))
        #node = int(x.index)

        if(ranking == 'degree'):
            node = searchInRanking(degreeRanking, seeds)
        if(ranking == 'betweenness'):
            node = searchInRanking(betweennessRanking, seeds)
        if(ranking == 'eigenvector'):
            node = searchInRanking(eigenvectorRanking, seeds)
        if (ranking == 'random'):
            node = searchInRanking(randomRanking, seeds)

        try:
            x = g.vs.find(str(node))
        except ValueError:
            Graph.add_vertex(g, str(node))
            x = g.vs.find(str(node))

        node = int(x.index)
        g.vs[int(node)]["infected"] = 1
        g.vs[int(node)]["stepinfected"] = 0
        g.vs[int(node)]["used"] = 0
        g.vs[int(node)]["color"] = "green"


    #### RANDOM FROM RANKING SCOPE ####

    #print('index', searchInRankingScope(createRanking(degreeRanking), int(random.uniform(0, degreeScope[len(degreeScope)-1]['value']))))
    #print('index', searchInRankingScope(createRanking(betweennessRanking), int(random.uniform(0, betweennessScope[len(betweennessScope)-1]['value']))))
    #print('index', searchInRankingScope(createRanking(eigenvectorRanking), float(random.uniform(0, eigenvectorScope[len(eigenvectorScope)-1]['value']))))
    #print('index', searchInRankingScope(createRanking(randomRanking), int(random.uniform(0, randomScope[len(randomScope)-1]['value']))))




    if(per == 'true'):
    #### ADD LINKS TO GRAPH ####
        for link in range(0, numberoflinks):
            if (linkRanking1 == 'degree'):
                node1 = searchInRankingScope(createRanking(degreeRanking), int(random.uniform(0, degreeScope[len(degreeScope)-1]['value'])))
            if (linkRanking2 == 'degree'):
                node2 = searchInRankingScope(createRanking(degreeRanking), int(random.uniform(0, degreeScope[len(degreeScope)-1]['value'])))
            if(linkRanking1 == 'betweenness'):
                node1 = searchInRankingScope(createRanking(betweennessRanking), int(random.uniform(0, betweennessScope[len(betweennessScope)-1]['value'])))
            if(linkRanking2 == 'betweenness'):
                node2 = searchInRankingScope(createRanking(betweennessRanking), int(random.uniform(0, betweennessScope[len(betweennessScope)-1]['value'])))
            if(linkRanking1 == 'eigenvector'):
                node1 = searchInRankingScope(createRanking(eigenvectorRanking), float(random.uniform(0, eigenvectorScope[len(eigenvectorScope)-1]['value'])))
            if(linkRanking2 == 'eigenvector'):
                node2 = searchInRankingScope(createRanking(eigenvectorRanking), float(random.uniform(0, eigenvectorScope[len(eigenvectorScope)-1]['value'])))
            if (linkRanking1 == 'random'):
                node1 = searchInRankingScope(createRanking(randomRanking), int(random.uniform(0, randomScope[len(randomScope)-1]['value'])))
            if (linkRanking2 == 'random'):
                node2 = searchInRankingScope(createRanking(randomRanking), int(random.uniform(0, randomScope[len(randomScope)-1]['value'])))
                #searchInRanking(randomRanking, link)
                #print(g.incident(searchInRanking(randomRanking, link), mode="out"))

            #print(node1)
            #if(node1['rank'] == 0):
            #    Graph.add_vertex(g, node1['name'])
            #if(node2['rank'] == 0):
            #    Graph.add_vertex(g, node2['name'])
            try:
                x1 = g.vs.find(str(node1))
            except ValueError:
                Graph.add_vertex(g, str(node1))
                x1 = g.vs.find(str(node1))

            try:
                x2 = g.vs.find(str(node2))
            except ValueError:
                Graph.add_vertex(g, str(node2))
                x2 = g.vs.find(str(node2))

            node1index = int(x1.index)
            node2index = int(x2.index)
            #print('wezel 1: ' + str(node1) + ', index: ' + str(node1index))
            #print('wezel 2: ' + str(node2) + ', index: ' + str(node2index))
            Graph.add_edge(g, node1index, node2index);

            #for edge in g.es:
                #source_vertex_id = edge.source
                #target_vertex_id = edge.target
                #source_vertex = g.vs[source_vertex_id]
                #target_vertex = g.vs[target_vertex_id]
                # using get_eid() you can do the opposite:
                #same_edge_id = g.get_eid(source_vertex_id, target_vertex_id)
                #same_edge = g.es[same_edge_id]
                # by .index you get the id from the Vertex or Edge object:
                #source_vertex.index == source_vertex_id
                # True
                #edge.index == same_edge_id
                # True
            #print('polaczenie z ', str(same_edge.source) + ' do ' +  str(same_edge.target) + '\n')
            #Graph.es[]

    ### WRITE TO FILE ###

    with writeInfectionsToFile:

        writeInfectionsFields = ['ranking', 'run', 'net', 'sp', 'pp', 'seed', 'step', 'infector', 'infected', 'infections', 'coverage', 'rank1', 'rank2', 'lp', 'permission']
        writer = csv.DictWriter(writeInfectionsToFile, fieldnames=writeInfectionsFields)
        #if(ranking == 'random'):
            #writer.writeheader()

    ### ###

        while(isInfecting):
            #print("STEP", s)
            infecting = infections
            nodes = Graph.vcount(g)
            for j in range(0,nodes):

                if (g.vs[j]["infected"] == 1 and g.vs[j]["used"] == 0 and g.vs[j]["stepinfected"] != s):
                    #print("INFEKUCJĄCY", g.vs[j]['name'])
                    writer.writerow({'ranking': ranking, 'run': run, 'net': net, 'sp': percentage,
                                     'pp': pp, 'seed': numberofseeds, 'step': s,
                                     'infector': g.vs[j]['name'],
                                     'infected': 0,
                                     'infections': infections,
                                     'coverage': 100 * (numberofseeds + infections) / nodes, 'rank1': rank1, 'rank2': rank2, 'lp': percentageLinks, 'permission': per})
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
                                    x = searchInArray(g.vs[j]['name'], g.vs[notinfected[k]]['name'], array)
                                    if(x == None):
                                        x = random.random()
                                    if(float(x) <= pp):
                                        g.vs[notinfected[k]]["infected"] = 1
                                        g.vs[notinfected[k]]["stepinfected"] = s
                                        g.vs[notinfected[k]]["used"] = 0
                                        g.vs[notinfected[k]]["color"] = "blue"

                                        #print("INFEKCJA",g.vs[j]['name'], g.vs[notinfected[k]]['name'], x, "\n\n")
                                        infections = infections + 1

                                        writer.writerow({'ranking': ranking, 'run': run, 'net': net, 'sp': percentage,
                                                         'pp': pp, 'seed': numberofseeds, 'step': s,
                                                         'infector': g.vs[j]['name'],
                                                         'infected': g.vs[notinfected[k]]['name'],
                                                         'infections': infections,
                                                         'coverage': 100 * (numberofseeds + infections) / nodes, 'rank1': rank1, 'rank2': rank2, 'lp': percentageLinks, 'permission': per})

            if(infecting == infections):
                isInfecting = False

            s = s + 1

        #plot(g)
        #print("Zainfekowanych", infections + numberofseeds)
        #print("Total coverage % (infections + seeds):")
        coverage = 100 * (numberofseeds + infections) / nodes
        return infections + numberofseeds, s - 1, coverage

resultArray = []

start = time.time()
#print("hello")



spARR = [0.01, 0.05]
lpARR = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
ppARR = [0.01, 0.05, 0.1, 0.15, 0.20, 0.25]
#ppARR = [0.01]


net = []


readPrefixes('syntetic/benchmark001/files.txt', net)

#myFile = open('syntetic/benchmark001/RESULTS/' + net[0][0:3] + 'result.csv', 'a')
#with myFile:
#    myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'ranking1', 'ranking2', 'lp']
#    writer = csv.DictWriter(myFile, fieldnames=myFields)
#    writer.writeheader();



ranking = ['random', 'degree', 'betweenness', 'eigenvector']
permission = ['true', 'false'];

for n in net:

    writeResultsToFile = open('syntetic/benchmark001/RESULTS/' + net[0][0:3] + 'result.csv', 'a')
    with writeResultsToFile:
        writeResultsFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'ranking1', 'ranking2', 'lp', 'permission']
        writer = csv.DictWriter(writeResultsToFile, fieldnames=writeResultsFields)
        writer.writeheader();

    writeInfectionsToFile = open('syntetic/benchmark001/INFECTIONS/' + n[0:3] + 'infections.csv', 'a')
    with writeInfectionsToFile:
        writeInfectionsFields = ['ranking', 'run', 'net', 'sp', 'pp', 'seed', 'step', 'infector', 'infected',
                                 'infections', 'coverage', 'rank1', 'rank2', 'lp', 'permission']
        writer1 = csv.DictWriter(writeInfectionsToFile, fieldnames=writeInfectionsFields)
        writer1.writeheader()

        for k in range(1, 9):
            writeResultsToFile = open('syntetic/benchmark001/RESULTS/' + net[0][0:3] + 'result.csv', 'a')
            with writeResultsToFile:
                myFields = ['ranking', 'run', 'net', 'sp', 'pp', 'step', 'infections', 'coverage', 'ranking1', 'ranking2', 'lp', 'permission']
                writer = csv.DictWriter(writeResultsToFile, fieldnames=myFields)
                for lp in lpARR:
                    for rank1 in ranking:
                        for rank2 in ranking:
                            for sp in spARR:
                                for pp in ppARR:
                                    for per in permission:
                                        for i in [1]:
                                            temp = simulation(pp, sp, n, rank1, i, lp, rank1, rank2, k, per)
                                            writer.writerow({'ranking': rank1, 'run': i, 'net': n + '_' + str(k), 'sp': sp, 'pp': pp,'step': temp[1],
                                                             'infections': temp[0], 'coverage': temp[2], 'ranking1': rank1, 'ranking2': rank2, 'lp': lp, 'permission': per})

end = time.time()
#print(end - start)

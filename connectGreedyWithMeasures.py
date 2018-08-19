import csv


greedyLinks = []
greedyLinksWithMeasures = []
maxLinks = []
maxLinksWithMeasures = []
randomLinks = []
randomLinksWithMeasures = []
results = []


with open('results/greedyToDisplay.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # print(row[0])
        if row != []:
            greedyLinks.append({'links': row[0],'coverage': row[1]})

with open('results/maxToDisplay.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # print(row[0])
        if row != []:
            maxLinks.append({'links': row[0],'coverage': row[1]})

with open('results/randomToDisplay.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # print(row[0])
        if row != []:
            randomLinks.append({'links': row[0],'coverage': row[1]})

with open('results/resultWithE.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # print(row)
        if row != []:
            results.append({'net': row[0], 'coverage': row[1], 'nodes': row[2], 'links': row[3][:-1], 'closeness': row[4], 'transitivity': row[5],
                             'eigenvector': row[6], 'betweenness': row[7]})


# for g in results:
    # print(g)

def search(link):
    for m in results:
        # print(m)
        if m['links'] == link:
            return m

myFile = open('results/readyToDisplayGreedy.csv', 'w')
myFile = open('results/readyToDisplayMax.csv', 'w')
myFile = open('results/readyToDisplayRandom.csv', 'w')

for g in greedyLinks:
    l = search(g['links'])
    print(l)
    myFile = open('results/readyToDisplayGreedy.csv', 'a+')
    with myFile:
        myFields = ['net', 'coverage', 'nodes', 'links', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow({'net': l['net'], 'coverage': l['coverage'], 'nodes': l['nodes'], 'links': l['links'], 'closeness': l['closeness'], 'transitivity': l['transitivity'],
                         'eigenvector': l['eigenvector'], 'betweenness': l['betweenness']})
for m in maxLinks:
    l = search(m['links'])
    myFile = open('results/readyToDisplayMax.csv', 'a+')
    with myFile:
        myFields = ['net', 'coverage', 'nodes', 'links', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow({'net': l['net'], 'coverage': l['coverage'], 'nodes': l['nodes'], 'links': l['links'], 'closeness': l['closeness'], 'transitivity': l['transitivity'],
                         'eigenvector': l['eigenvector'], 'betweenness': l['betweenness']})

for r in randomLinks:
    l = search(r['links'])
    myFile = open('results/readyToDisplayRandom.csv', 'a+')
    with myFile:
        myFields = ['net', 'coverage', 'nodes', 'links', 'closeness', 'transitivity', 'eigenvector', 'betweenness']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow({'net': l['net'], 'coverage': l['coverage'], 'nodes': l['nodes'], 'links': l['links'], 'closeness': l['closeness'], 'transitivity': l['transitivity'],
                         'eigenvector': l['eigenvector'], 'betweenness': l['betweenness']})

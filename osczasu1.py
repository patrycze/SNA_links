from datetime import datetime, timedelta
import collections
import csv

myFile = open('results/usersClassification.csv', 'w')


def classify(product):
    if (product.percent < 2.5):
        product.title = 'innovator'
        # print('innnovator < 2.5%')
    if (product.percent > 2.5 and product.percent < 16):
        product.title = 'early adopter'
        # print('early adopter > 2.5% and < 16%')
    if (product.percent > 16 and product.percent < 50):
        product.title = 'early majority'
        # print('early majority > 16% and < 50%')
    if (product.percent > 50 and product.percent < 84):
        product.title = 'late majority'
        # print('late majority > 50% and < 84%')
    if (product.percent > 84):
        product.title = 'laggards'
        # print('laggards > 84%')



class ProductsDictionary:

    id = ''
    products = []
    scope = ''
    last = ''

    def calculatePercentage(self, value):
        if(self.scope != 0):
            return float(value.total_seconds()) * 100 / float(self.scope)
        else:
            return 0
    def assignPerctentage(self):
        for product in self.products:
            product.percent = self.calculatePercentage(self.last - product.date)

    def assignTitle(self):
        for product in self.products:
            classify(product)
class Product:

    id = ''
    time = ''
    user = ''
    percent = ''
    title = ''



name = 'Early_adopters_7_step_1_d'

productsList = []

with open(name + '.csv', "r") as rows:
    for row in rows:

        # row[:-2] wycina znak spacji na koncu
        row = row[:-2].split(";")

        product = Product()

        product.id = row[2]
        # print(row[4], row[5])
        product.date = datetime.strptime(row[4] + ' ' + row[5], "%Y-%m-%d %H:%M:%S")
        product.user = row[6]

        productsList.append(product)

        # print(product.date)



productsDictionary = ProductsDictionary()

productList = list(set([p.id for p in productsList]))
productDict = collections.OrderedDict.fromkeys(set([p.id for p in productsList]))

for key, value in productDict.items():
    # productDict[key] = [pL for pL in productsList if pL.id == key]
    productDict[key] = [pL for pL in productsList if pL.id == str(key)]

allProducts = []

for key, value in productDict.items():
    productsDictionary = ProductsDictionary()
    productsDictionary.products = productDict[key]
    productsDictionary.scope = productDict[key][len(productDict[key])-1].date - productDict[key][0].date
    productsDictionary.last = productDict[key][len(productDict[key])-1].date
    productsDictionary.scope = productsDictionary.scope.total_seconds()
    productsDictionary.assignPerctentage()
    productsDictionary.assignTitle()
    allProducts.append(productsDictionary)

myFields = ['prod_id', 'user_id', 'title']

myFile = open('results/usersClassification.csv', 'a+')
with myFile:
    writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
    writer.writeheader()

for productsDictionary in allProducts:
    for prod in reversed(productsDictionary.products):
        myFile = open('results/usersClassification.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow({'prod_id': prod.id, 'user_id': prod.user, 'title': prod.title})

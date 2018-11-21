from datetime import datetime, timedelta
import collections
import csv

myFile = open('results/usersClassification.csv', 'w')


def classify(product):
    if(isinstance(product.percent, float)):
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
            return float(value) * 100 / float(self.scope)
        else:
            return 0
    def assignPerctentage(self):
        for product in self.products:
            # print('assign', type(product.order_id))
            if(isinstance(product.order_id, int)):
                product.percent = self.calculatePercentage(product.order_id)

    def assignTitle(self):
        for product in self.products:
            classify(product)
class Product:

    id = ''
    time = ''
    user = ''
    percent = ''
    title = ''
    limit = ''
    order_id = ''
    date = ''
    friends = ''
    logs= ''
    msg_sum = ''

name = 'data'

productsList = []

with open(name + '.csv', "r") as rows:
    for row in rows:
        # row[:-2] wycina znak spacji na koncu
        row = row[:-2].split(";")

        product = Product()

        product.id = row[2]
        product.date = datetime.strptime(row[4].replace("\"","") + ' ' + row[5].replace("\"",""), "%Y-%m-%d %H:%M:%S")
        product.user = row[6]
        product.friends = row[7]
        product.logs = row[13]
        product.msg_sum = float(row[10]) + float(row[11])
        product.limit = datetime.strptime(row[9].replace("\"",""), "%Y-%m-%d %H:%M")
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

    # tutaj liczba uzytkownikow do danego momentu
    productsDictionary.scope = len([value for counter, value in enumerate(productDict[key]) if value.date < value.limit])
    # tutaj przypisuje uzytkownikom order_id
    counter = 0
    for value in productDict[key]:
        if value.date < value.limit:
            value.order_id = counter + 1;
            counter = counter + 1
            print('ORDER ID', value.order_id, 'DLA ITEMU O ID ', value.id,
                  'I UZYTKOWNIKA', value.user, ' DATA ZMIANY ', value.date, 'DATA WYGASNIECIA PRODUKTU ', value.limit)

    productsDictionary.products = productDict[key]

    productsDictionary.last = productDict[key][len(productDict[key])-1].date
    # productsDictionary.scope = productsDictionary.scope.total_seconds()
    productsDictionary.assignPerctentage()
    productsDictionary.assignTitle()
    allProducts.append(productsDictionary)


myFields = ['prod_id', 'user_id', 'title', 'date', 'limit', 'percentage', 'friends', 'logs', 'mgs_sum']

myFile = open('results/usersClassification.csv', 'a+')
with myFile:
    writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
    writer.writeheader()

for productsDictionary in allProducts:
    for prod in reversed(productsDictionary.products):
        myFile = open('results/usersClassification.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow({'prod_id': prod.id, 'user_id': prod.user, 'title': prod.title, 'date': prod.date,
                             'limit': prod.limit, 'percentage': prod.percent,
                             'friends': prod.friends, 'logs': prod.logs, 'mgs_sum': prod.msg_sum})

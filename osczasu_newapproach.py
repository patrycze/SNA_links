from datetime import datetime, timedelta
import collections
import csv

myFile = open('results/usersClassification.csv', 'w')


def classify(product):
    if(isinstance(product.percent, float)):
        if (product.percent <= 2.5):
            product.title = 'innovator'
            # print('innnovator < 2.5%')
        if (product.percent > 2.5 and product.percent <= 16):
            product.title = 'early adopter'
            # print('early adopter > 2.5% and < 16%')
        if (product.percent > 16 and product.percent <= 50):
            product.title = 'early majority'
            # print('early majority > 16% and < 50%')
        if (product.percent > 50 and product.percent <= 84):
            product.title = 'late majority'
            # print('late majority > 50% and < 84%')
        if (product.percent >= 84):
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
    v1 = ''
    v2 = ''
    v3 = ''
    v4 = ''
    v5 = ''
    day = ''
    first_usage = ''
    life_class = ''

name = 'data'

productsList = []

with open(name + '.csv', "r") as rows:
    for row in rows:


            # row[:-2] wycina znak spacji na koncu
        row = row[:-2].split(";")

        # print(len(row[9]))

        if len(row[10]) > 2 :

            product = Product()

            product.cd = row[0]
            product.day = row[3]
            product.element_type = row[1]
            product.id = row[2]
            product.date = datetime.strptime(row[9].replace("'",""), "%Y-%m-%d %H:%M:%S")
            product.user = row[6]
            product.friends = ''
            product.logs = ''
            product.v3 = row[13]
            product.v4 = row[14]
            product.v2 = row[16]
            product.v1 = row[17]
            product.v5 = row[18]
            product.life_class = row[11]
            product.first_usage = row[19]
            # product.firstusage = row[]
            # product.msg_sum = float(row[10]) + float(row[11])
            product.limit = datetime.strptime(row[10].replace("'",""), "%Y-%m-%d %H:%M")
            productsList.append(product)

            # print(product.date)



productsDictionary = ProductsDictionary()

productCustomHash = {}

productList = list(set([p.id for p in productsList]))
productDict = collections.OrderedDict.fromkeys(set([p.id for p in productsList]))
cd_dict = collections.OrderedDict.fromkeys(set([p.cd for p in productsList]))
element_type_dict = collections.OrderedDict.fromkeys(set([p.element_type for p in productsList]))

# for key, value in productDict.items():
#     # productDict[key] = [pL for pL in productsList if pL.id == key]
#     productDict[key] = [pL for pL in productsList if pL.id == str(key)]

for key, value in cd_dict.items():
    cd_dict[key] = [pL for pL in productsList if pL.cd == str(key)]


for key_cd, value_cd in cd_dict.items():
    for key_et, value_et in element_type_dict.items():
        for key_id, value_id in productDict.items():
            productCustomHash[str(key_cd) + str(key_et) + str(key_id)] = []
            for product in productsList:
                if(product.cd == key_cd and product.element_type == key_et and product.id == key_id):
                    productCustomHash[str(key_cd) + str(key_et) + str(key_id)].append(product)

allProducts = []






for key, value in productCustomHash.items():
    productsDictionary = ProductsDictionary()

    # tutaj liczba uzytkownikow do danego momentu
    productsDictionary.scope = len([value for counter, value in enumerate(productCustomHash[key]) if value.date < value.limit])
    # tutaj przypisuje uzytkownikom order_id
    counter = 0
    for value in productCustomHash[key]:
        if value.date < value.limit:
            value.order_id = counter + 1;
            counter = counter + 1

    productsDictionary.products = productCustomHash[key]
    if(len(productCustomHash[key]) > 0):
        productsDictionary.last = productCustomHash[key][len(productCustomHash[key])-1].date
        productsDictionary.assignPerctentage()
        productsDictionary.assignTitle()
        allProducts.append(productsDictionary)


myFields = ['cd', 'element_type', 'prod_id', 'user_id', 'title', 'date', 'limit', 'percentage', 'day', 'life_class', 'first_usage', 'friends', 'logs', 'mgs_sum', 'v1', 'v2', 'v3', 'v4', 'v5']

myFile = open('results/usersClassification.csv', 'a+')
with myFile:
    writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
    writer.writeheader()

for productsDictionary in allProducts:
    for prod in reversed(productsDictionary.products):
        myFile = open('results/usersClassification.csv', 'a+')
        with myFile:
            writer = csv.DictWriter(myFile, restval=0, fieldnames=myFields, extrasaction='ignore')
            writer.writerow({'cd':prod.cd, 'element_type': prod.element_type, 'prod_id': prod.id, 'user_id': prod.user, 'title': prod.title, 'date': prod.date,
                             'limit': prod.limit, 'percentage': prod.percent, 'day': prod.day, 'life_class': prod.life_class, 'first_usage': prod.first_usage,
                             'friends': prod.friends, 'logs': prod.logs, 'mgs_sum': prod.msg_sum, 'v1': prod.v1,'v2': prod.v2,'v3': prod.v3,'v4': prod.v4,'v5': prod.v5})

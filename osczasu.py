from datetime import datetime, timedelta

class ProductsDictionary:

    id = ''
    products = []
    scope = ''
    last = ''

    def calculatePercentage(self, value):
        return float(value.total_seconds()) * 100 / float(self.scope)

    def assignPerctentage(self):
        for product in self.products:
            product.percent = self.calculatePercentage(self.last - product.date)
            print(product.percent)

    def assignTitle(self):
        for product in self.products:

class Product:

    id = ''
    time = ''
    user = ''
    percent = ''
    title = ''


def classify(product):
    if (value < 2.5):
        product.title = 'innnovator'
        # print('innnovator < 2.5%')
    if (value > 2.5 and value < 16):
        product.title = 'early adopter'
        # print('early adopter > 2.5% and < 16%')
    if (value > 16 and value < 50):
        product.title = 'early majority'
        # print('early majority > 16% and < 50%')
    if (value > 50 and value < 84):
        product.title = 'late majority'
        # print('late majority > 50% and < 84%')
    if (value > 84):
        product.title = 'laggards'
        # print('laggards > 84%')


name = 'Early_adopters_7_step_1_d'

productsList = []

with open(name + '.csv', "r") as rows:
    for row in rows:

        # row[:-2] wycina znak spacji na koncu
        row = row[:-2].split(";")

        product = Product()

        product.id = row[2]
        product.date = datetime.strptime(row[4] + ' ' + row[5], "%Y-%m-%d %H:%M:%S")
        product.user = row[6]

        productsList.append(product)

        # print(product.date)



productsDictionary = ProductsDictionary()

productsDictionary.products = productsList
productsDictionary.scope = productsList[len(productsList)-1].date - productsList[0].date
productsDictionary.last = productsList[len(productsList)-1].date
productsDictionary.scope = productsDictionary.scope.total_seconds()

# print(productsList[len(productsList)-1].date - productsList[0].date)


productsDictionary.assignPerctentage()
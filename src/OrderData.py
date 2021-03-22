import csv
import os
from datetime import datetime
import locale
import re
from src.Entities import Restaurant, Product, Address, Customer, Order, Coupon
from src.database import Database


class OrderData:
    SKIP_ROWS = 4

    def __init__(self, fileName):
        self.fileName = fileName
        self.database = Database()

    def process(self):
        with open(os.getcwd() + "/watch/" + self.fileName, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for _ in range(self.SKIP_ROWS):
                next(csv_reader)
            headers = next(csv_reader)
            print(headers)
            orders = []

            currentOrder = []
            for order in csv_reader:
                if len(order) > 0:
                    if order[headers.index('Totaalprijs')] != '':
                        if currentOrder:
                            orders.append(currentOrder)
                            currentOrder = []
                    currentOrder.append(order)

            import time
            start = time.time()
            for order in orders:
                restaurantName = order[0][headers.index('Winkelnaam')]
                restaurantId = Restaurant.getStoreByName(self.database, restaurantName)
                customerName = order[0][headers.index('Klantnaam')]
                customerPhoneNr = order[0][headers.index('TelefoonNr')]
                customerEmail = order[0][headers.index('Email')]
                address = order[0][headers.index('Adres')]
                city = order[0][headers.index('Woonplaats')]
                # addressId = Address.getOrCreateAddress(self.database, address, city)
                addressId = 10590
                customerId = Customer.createOrUpdateCustomer(self.database, customerEmail, customerName,
                                                             customerPhoneNr, addressId)
                orderDate = parseDate(order[0][headers.index('Besteldatum')])
                deliveryTypeString = order[0][headers.index('AfleverType')]
                if deliveryTypeString == 'Bezorgen':
                    deliveryType = True
                elif deliveryTypeString == 'Afhalen':
                    deliveryType = False
                else:
                    raise Exception('Niet bekend delivery type')
                    #TODO
                deliveryDate = parseDate(order[0][headers.index('AfleverDatum')])
                deliveryTime = order[0][headers.index('AfleverMoment')]
                if re.match('^([0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', deliveryTime):
                    hour, minute = deliveryTime.split(':')
                    deliveryDate = deliveryDate.replace(hour=int(hour), minute=int(minute))
                totalPrice = priceToFloat(order[0][headers.index('Totaalprijs')])
                couponName = order[0][headers.index('Gebruikte Coupon')]
                couponId = Coupon.getCouponByName(couponName)
                couponDiscount = priceToFloat(order[0][headers.index('Coupon Korting')])
                paymentAmount = priceToFloat(order[0][headers.index('Te Betalen')])
                if restaurantId is not None:
                    orderId = Order.createOrder(self.database, restaurantId, customerId, deliveryType, couponDiscount,
                                                orderDate, deliveryDate, couponId)
                else:
                    print(restaurantName)

                for orderRow in order:
                    productName = orderRow[headers.index('Product')]
                    crustName = orderRow[headers.index('PizzaBodem')]
                    crustId = Product.getPizzaCrustByName(self.database, crustName)
                    sauceName = orderRow[headers.index('PizzaSaus')]
                    sauceId = Product.getSauceByName(self.database, sauceName)
                    if crustName == '' and sauceName == '':
                        otherProductId = Product.getOtherProductIdByName(self.database, productName)
                        pizzaId = None
                    else:
                        pizzaId = Product.getPizzaIdByName(self.database, productName)
                        otherProductId = None
                    price = priceToFloat(orderRow[headers.index('Prijs')])
                    deliveryCosts = priceToFloat(orderRow[headers.index('Bezorgkosten')])
                    amount = int(orderRow[headers.index('Aantal')])
                    extraIngredientString = orderRow[headers.index('Extra Ingrediënten')]
                    if len(extraIngredientString.strip()) > 0:
                        extraIngredients = [Product.getIngredientByName(self.database, ingredient.strip()) for ingredient in
                                            extraIngredientString.split(',')]
                    else:
                        extraIngredients = []
                    priceExtraIngredients = priceToFloat(orderRow[headers.index('Prijs Extra Ingrediënten')])
                    orderRowPrice = priceToFloat(orderRow[headers.index('Regelprijs')])
                    print(otherProductId)
                    Order.createOrderLine(self.database, orderId, orderRowPrice, amount, extraIngredients, sauceId, crustId, pizzaId,
                                          otherProductId)

            self.database.conn.commit()

            print(time.time() - start)

            print(len(orders))


def priceToFloat(priceString):
    if priceString == '' or priceString is None:
        return None
    cleanString = ''.join(ch for ch in priceString if ch.isdigit() or ch == ',').replace(',', '.')
    if cleanString:
        return float(cleanString)
    else:
        return None

def parseDate(dateString):
    locale.setlocale(locale.LC_ALL, 'nl_NL')
    date = datetime.strptime(' '.join(dateString.split(' ')[1:]), '%d %B %Y')
    locale.setlocale(locale.LC_ALL, '')
    return date

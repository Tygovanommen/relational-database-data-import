import csv
import os
from datetime import datetime
import time
import locale
import re
from src.Entities import Restaurant, Product, Address, Customer, Order, Coupon
from src.database import Database
from src.logger import Logger


class OrderData:
    SKIP_ROWS = 4

    def __init__(self, fileName):
        self.fileName = fileName
        self.database = Database()
        self.logger = Logger()
        self.invalidOrders = 0

    def process(self):
        self.logger.info('Starting OrderData import')
        with open(os.getcwd() + "/watch/" + self.fileName, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for _ in range(self.SKIP_ROWS):
                next(csv_reader)
            headers = next(csv_reader)
            orders = []

            rowCount = self.SKIP_ROWS
            currentOrder = []
            for order in csv_reader:
                rowCount += 1
                if len(order) > 0:
                    if order[headers.index('Totaalprijs')] != '':
                        if currentOrder:
                            orders.append(currentOrder)
                            currentOrder = []
                    currentOrder.append(order + [rowCount])

            start = time.time()
            self.logger.info("Processing {} orders".format(len(orders)))
            self.createOrderObj(headers, orders)

            self.logger.info('Import completed in: {}'.format(time.time() - start))
            self.logger.info('Invalid orders: {}'.format(self.invalidOrders))

    def createOrderObj(self, headers, orders):
        for order in orders:
            restaurantName = order[0][headers.index('Winkelnaam')]
            restaurantId = Restaurant.getStoreByName(self.database, restaurantName)
            customerName = order[0][headers.index('Klantnaam')]
            customerPhoneNr = order[0][headers.index('TelefoonNr')]
            customerEmail = order[0][headers.index('Email')]
            address = order[0][headers.index('Adres')]
            city = order[0][headers.index('Woonplaats')]
            addressId = Address.getOrCreateAddress(self.database, address, city)

            customerId = Customer.createOrUpdateCustomer(self.database, customerEmail, customerName,
                                                         customerPhoneNr, addressId)
            orderDate = parseDate(order[0][headers.index('Besteldatum')])
            deliveryTypeString = order[0][headers.index('AfleverType')]
            if deliveryTypeString == 'Bezorgen':
                deliveryType = True
            elif deliveryTypeString == 'Afhalen':
                deliveryType = False
            else:
                deliveryType = None

            deliveryDate = parseDate(order[0][headers.index('AfleverDatum')])
            deliveryTime = order[0][headers.index('AfleverMoment')]
            if re.match('^([0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', deliveryTime):
                hour, minute = deliveryTime.split(':')
                deliveryDate = deliveryDate.replace(hour=int(hour), minute=int(minute))
            totalPrice = priceToFloat(order[0][headers.index('Totaalprijs')])
            couponName = order[0][headers.index('Gebruikte Coupon')].strip()
            if len(couponName) > 0:
                couponId = Coupon.createCouponIfNotExists(self.database, couponName)
            else:
                couponId = None
            couponDiscount = priceToFloat(order[0][headers.index('Coupon Korting')])
            paymentAmount = priceToFloat(order[0][headers.index('Te Betalen')])

            orderObj = Order.Order(restaurantId, customerId, deliveryType, couponDiscount,
                                   orderDate, deliveryDate, couponId, rowNumber=order[0][-1])

            for orderRow in order:
                productName = orderRow[headers.index('Product')].strip()
                crustName = orderRow[headers.index('PizzaBodem')]
                crustId = Product.getPizzaCrustByName(self.database, crustName)
                sauceName = orderRow[headers.index('PizzaSaus')]
                sauceId = Product.getSauceByName(self.database, sauceName)
                if crustName == '' and sauceName == '':
                    otherProductId = Product.getOtherProductIdByName(self.database, productName)
                    pizzaId = None
                else:
                    pizzaId = Product.getPizzaIdByName(self.database, productName)
                    if pizzaId is None:
                        pass
                    otherProductId = None
                price = priceToFloat(orderRow[headers.index('Prijs')])
                deliveryCosts = priceToFloat(orderRow[headers.index('Bezorgkosten')])
                amount = int(orderRow[headers.index('Aantal')])
                extraIngredientString = orderRow[headers.index('Extra Ingrediënten')]
                if len(extraIngredientString.strip()) > 0:
                    extraIngredients = [Product.getIngredientByName(self.database, ingredient.strip()) for
                                        ingredient in
                                        extraIngredientString.split(',')]
                else:
                    extraIngredients = []
                priceExtraIngredients = priceToFloat(orderRow[headers.index('Prijs Extra Ingrediënten')])
                orderRowPrice = priceToFloat(orderRow[headers.index('Regelprijs')])

                orderLine = Order.OrderLine(orderRowPrice, amount, extraIngredients, sauceId, crustId, pizzaId,
                                            otherProductId, rowNumber=orderRow[-1])

                orderObj.addOrderLine(orderLine)

            self.createOrder(orderObj)

    def createOrder(self, orderObj):
        orderValid, orderErrors, = orderObj.isValid()
        if orderValid:
            orderId = Order.createOrder(self.database, orderObj)
            for orderLine in orderObj.orderLines:
                Order.createOrderLine(self.database, orderLine, orderId)
        else:
            self.logger.error(
                'Order not valid row: {}, error: {}'.format(orderObj.rowNumber, ', '.join(orderErrors)))

            for row in orderObj.orderLines:
                rowValid, rowErrors = row.isValid()
                if not rowValid:
                    self.logger.error(
                        'Order line not valid row: {}, error: {}'.format(row.rowNumber, ', '.join(rowErrors)))

            self.invalidOrders += 1


def priceToFloat(priceString):
    if priceString == '' or priceString is None:
        return None
    cleanString = ''.join(ch for ch in priceString if ch.isdigit() or ch == ',').replace(',', '.')
    if cleanString:
        return float(cleanString)
    else:
        return None


def parseDate(dateString):
    try:
        locale.setlocale(locale.LC_ALL, 'nl_NL')
        date = datetime.strptime(' '.join(dateString.split(' ')[1:]), '%d %B %Y')
        locale.setlocale(locale.LC_ALL, '')
    except:
        return None
    return date

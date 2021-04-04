import datetime


class Order:
    def __init__(self, restaurant_id, customer_id, delivery, coupon_discount_amount, created_at, completed_at,
                 coupon_id=None, rowNumber=None):
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id
        self.delivery = delivery
        self.coupon_discount_amount = coupon_discount_amount
        self.created_at = created_at
        self.completed_at = completed_at
        self.coupon_id = coupon_id
        self.rowNumber = rowNumber
        self.orderLines = []

    def addOrderLine(self, orderLine):
        self.orderLines.append(orderLine)

    def isValid(self):
        valid = True
        errors = []
        if not self.restaurant_id:
            valid = False
            errors.append('Restaurant is not set.')
        if not self.customer_id:
            valid = False
            errors.append('Customer is not set.')
        if self.delivery is None:
            valid = False
            errors.append('Not a valid delivery option.')
        if not isinstance(self.created_at, datetime.datetime):
            valid = False
            errors.append('Created at not a valid datetime.')
        if not isinstance(self.completed_at, datetime.datetime):
            valid = False
            errors.append('Completed at not a valid datetime.')
        for orderLine in self.orderLines:
            orderLineValid, orderLineErrors = orderLine.isValid()
            if orderLineValid is False:
                valid = False
                errors.append('Orderline not valid.')

        return valid, errors


class OrderLine:
    def __init__(self, price, quantity, extra_ingredients, sauce_id, crust_id, pizza_id, other_product_id, rowNumber=None):
        self.price = price
        self.quantity = quantity
        self.extra_ingredients = extra_ingredients
        self.sauce_id = sauce_id
        self.crust_id = crust_id
        self.pizza_id = pizza_id
        self.other_product_id = other_product_id
        self.rowNumber = rowNumber

    def isValid(self):
        valid = True
        errors = []

        if self.price is None:
            valid = False
            errors.append('No price entered.')
        if self.quantity is None:
            valid = False
            errors.append('No quantity.')
        for ingredient in self.extra_ingredients:
            if ingredient is None:
                valid = False
                errors.append('Ingredient not found.')
                break
        if self.pizza_id is None and self.other_product_id is None:
            valid = False
            errors.append('Product not found.')
        if self.pizza_id and self.crust_id is None:
            valid = False
            errors.append('Pizza crust not found.')
        if self.pizza_id and self.sauce_id is None:
            valid = False
            errors.append('Pizza sauce not found.')

        return valid, errors


def createOrder(database, order):
    with database.cursor as cursor:
        query = '''INSERT INTO [dbo].[order](restaurant_id, customer_id, coupon_id, delivery, coupon_discount_amount, created_at, completed_at)
                   OUTPUT Inserted.ID
                   VALUES(?,?,?,?,?,?,?)'''
        args = [order.restaurant_id,
                order.customer_id,
                order.coupon_id,
                order.delivery,
                order.coupon_discount_amount,
                order.created_at,
                order.completed_at]

        orderId = int(cursor.execute(query, args).fetchone()[0])

        return orderId


def createOrderLine(database, orderLine, orderId):
    with database.cursor as cursor:
        query = '''INSERT INTO order_line(order_id, custom_sauce_product_id, crust_product_id, pizza_product_id, other_product_id, price, quantity) 
                   OUTPUT Inserted.ID
                   VALUES(?,?,?,?,?,?,?)'''

        args = [orderId,
                orderLine.sauce_id,
                orderLine.crust_id,
                orderLine.pizza_id,
                orderLine.other_product_id,
                orderLine.price,
                orderLine.quantity]

        orderLineId = int(cursor.execute(query, args).fetchone()[0])
        ingredientDict = {}
        for ingredient in orderLine.extra_ingredients:
            if ingredient not in ingredientDict:
                ingredientDict[ingredient] = 1
            else:
                ingredientDict[ingredient] += 1
        for ingredient in ingredientDict:
            query = 'INSERT INTO custom_pizza_ingredient(custom_ingredient_product_id, order_line_id, amount) VALUES(?,?,?)'
            args = [ingredient, orderLineId, ingredientDict[ingredient]]
            cursor.execute(query, args)
        return orderLineId

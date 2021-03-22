def createOrder(database, restaurant_id, customer_id, delivery, coupon_discount_amount, created_at, completed_at, coupon_id=None):
    with database.cursor as cursor:
        query = 'INSERT INTO [dbo].[order](restaurant_id, customer_id, coupon_id, delivery, coupon_discount_amount, created_at, completed_at) VALUES(?,?,?,?,?,?,?)'
        args = [restaurant_id, customer_id, coupon_id, delivery, coupon_discount_amount, created_at, completed_at]
        print(args)
        cursor.execute(query, args)

        id = int(cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0])
        return id


def createOrderLine(database, order_id, price, quantity, extra_ingredients, sauce_id, crust_id,
                    pizza_id, other_product_id):
    with database.cursor as cursor:
        query = 'INSERT INTO order_line(order_id, custom_sauce_product_id, crust_product_id, pizza_product_id, other_product_id, price, quantity) VALUES(?,?,?,?,?,?,?)'
        args = [order_id, sauce_id, crust_id, pizza_id, other_product_id, price, quantity]
        print(other_product_id)
        print(args)
        cursor.execute(query, args)
        id = int(cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0])
        ingredientDict = {}
        for ingredient in extra_ingredients:
            if ingredient not in ingredientDict:
                ingredientDict[ingredient] = 1
            else:
                ingredientDict[ingredient] += 1
        for ingredient in ingredientDict:
            query = 'INSERT INTO custom_pizza_ingredient(custom_ingredient_product_id, order_line_id, amount) VALUES(?,?,?)'
            args = [ingredient, id, ingredientDict[ingredient]]
            cursor.execute(query, args)
        return id


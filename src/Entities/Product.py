from src.database import Database

crustDict = {}


def getPizzaCrustByName(database, crustName):
    crustName = crustName.upper()
    if crustName in crustDict:
        return crustDict.get(crustName)
    with database.cursor as cursor:
        query = ("SELECT\n"
                 "   product.id \n"
                 "FROM\n"
                 "   category \n"
                 "   LEFT JOIN\n"
                 "      product \n"
                 "      ON category.id = product.category_id \n"
                 "      AND date_to IS NULL \n"
                 "WHERE\n"
                 "   category.category_name = 'Pizza Crusts' \n"
                 "AND product.product_name = ?")

        args = (crustName)
        for row in cursor.execute(query, args).fetchall():
            crustDict[crustName] = row.id
            return row.id

        return None


sauceDict = {}


def getSauceByName(database, sauceName):
    sauceName = sauceName.upper()
    if sauceName in sauceDict:
        return sauceDict.get(sauceName)
    with database.cursor as cursor:
        query = ("SELECT\n"
                 "   product.id \n"
                 "FROM\n"
                 "   category \n"
                 "   LEFT JOIN\n"
                 "      product \n"
                 "      ON category.id = product.category_id \n"
                 "      AND date_to IS NULL \n"
                 "WHERE\n"
                 "   category.category_name = 'Pizza Sauces' \n"
                 "AND product.product_name = ?")

        args = (sauceName)
        for row in cursor.execute(query, args).fetchall():
            sauceDict[sauceName] = row.id
            return row.id

        return None


def getOtherProductIdByName(database, productName):
    # TODO
    return None


ingredientDict = {}


def getIngredientByName(database, ingredientName):
    ingredientName = ingredientName.upper()
    if ingredientName in ingredientDict:
        return ingredientDict.get(ingredientName)
    with database.cursor as cursor:
        query = ("SELECT\n"
                 "   product.id \n"
                 "FROM\n"
                 "   category \n"
                 "   LEFT JOIN\n"
                 "      product \n"
                 "      ON category.id = product.category_id \n"
                 "      AND date_to IS NULL \n"
                 "WHERE\n"
                 "   category.category_name = 'Pizza Ingredients' \n"
                 "AND product.product_name = ?")

        args = (ingredientName)
        for row in cursor.execute(query, args).fetchall():
            ingredientDict[ingredientName] = row.id
            return row.id

        return None


pizzaDict = {}


def getPizzaIdByName(database, pizzaName):
    pizzaName = pizzaName.upper()
    if pizzaName in pizzaDict:
        return pizzaDict.get(pizzaName)
    with database.cursor as cursor:
        query = ("SELECT pizza.product_id\n"
                 "FROM pizza\n"
                 "INNER JOIN product ON pizza.product_id = product.id AND product.date_to IS NULL\n"
                 "WHERE UPPER(product.product_name) LIKE UPPER(?)")

        args = (pizzaName)
        for row in cursor.execute(query, args):
            pizzaDict[pizzaName] = row.product_id
            return row.product_id

        return None



from src.database import Database

restaurantDict = {}


def getStoreByName(database, name):
    if name in restaurantDict:
        return restaurantDict.get(name)
    with database.cursor as cursor:
        query = 'SELECT id, name FROM restaurant WHERE UPPER(name) LIKE UPPER(?)'
        args = (name)
        for row in cursor.execute(query, args):
            restaurantDict[name] = row.id
            return row.id

        return None

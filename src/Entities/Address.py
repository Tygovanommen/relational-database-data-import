adresDict = {}

def getOrCreateAddress(database, address, city):
    if address + city in adresDict:
        return adresDict[address + city]
    with database.cursor as cursor:
        query = "SELECT id FROM other_address WHERE address = ? AND city = ?"
        args = [address, city]
        for row in cursor.execute(query, args).fetchall():
            adresDict[address + city] = row.id
            return row.id

        query = """INSERT INTO other_address(address, city)
                    OUTPUT inserted.id
                    VALUES(?, ?)"""
        args = [address, city]
        addressId = cursor.execute(query, args).fetchone()[0]
        adresDict[address + city] = addressId
        return addressId
    return None


couponTypeId = None
def getImportCouponTypeId(database):
    if couponTypeId is not None:
        return couponTypeId

    with database.cursor as cursor:
        query = "SELECT id FROM coupon_type WHERE type_name = 'IMPORTED'"
        for row in cursor.execute(query):
            return row.id
        query = """INSERT INTO coupon_type(type_name, type_description) 
                    OUTPUT inserted.id
                    VALUES('IMPORTED', 'IMPORTED')"""
        return cursor.execute(query).fetchone()[0]



couponDict = {}
def createCouponIfNotExists(database, couponName):
    couponName = couponName.upper()
    if couponName in couponDict:
        return couponDict[couponName]

    with database.cursor as cursor:
        query = 'SELECT id FROM coupon WHERE name = ?'
        args = [couponName]
        for row in cursor.execute(query, args):
            couponDict[couponName] = row.id
            return row.id

        query = '''INSERT INTO coupon(coupon_type_id, name, discription, coupon_nr, date_from, date_to)
                   OUTPUT inserted.id
                   VALUES(?, ?, '', -1, GETDATE(), GETDATE())'''
        args = [getImportCouponTypeId(database), couponName]
        id = cursor.execute(query, args).fetchone()[0]
        couponDict[couponName] = id
        return id
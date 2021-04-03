from src.database import Database


def createOrUpdateCustomer(database, email, name, phoneNr, addressId):
    with database.cursor as cursor:
        query = 'SELECT id FROM customer WHERE UPPER(email_adress) LIKE UPPER(?)'
        args = (email)
        for row in cursor.execute(query, args).fetchall():
            query = 'UPDATE customer SET name = ?, phone_nr = ? WHERE id = ?'
            args = [name, phoneNr, row.id]
            cursor.execute(query, args)

            query = """IF NOT EXISTS(SELECT * FROM customer_adress WHERE other_adress_id = ? AND customer_id = ?)
                        BEGIN
                        INSERT INTO customer_adress(other_adress_id, customer_id) VALUES(?, ?) 
                        END
                        """
            args = [addressId, row.id, addressId, row.id]
            cursor.execute(query, args)
            return row.id

        query = '''INSERT INTO customer(name, phone_nr, email_adress)
                   OUTPUT inserted.ID
                   VALUES(?, ?, ?)'''
        args = (name, phoneNr, email)
        id = cursor.execute(query, args).fetchone()[0]
        return id





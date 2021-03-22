from src.database import Database


def createOrUpdateCustomer(database, email, name, phoneNr, addressId):
    with database.cursor as cursor:
        query = 'SELECT id FROM customer WHERE UPPER(email_adress) LIKE UPPER(?)'
        args = (email)
        for row in cursor.execute(query, args):
            query = 'UPDATE customer SET name = ?, phone_nr = ? WHERE id = ?'
            args = [name, phoneNr, row.id]
            cursor.execute(query, args)

            query = """IF NOT EXISTS(SELECT * FROM customer_adress WHERE adress_id = ? AND customer_id = ?)
                        BEGIN
                        INSERT INTO customer_adress(adress_id, customer_id) VALUES(?, ?) 
                        END
                        """
            args = [addressId, row.id, addressId, row.id]
            # cursor.execute(query, args)
            database.conn.commit()
            return row.id

        query = 'INSERT INTO customer(name, phone_nr, email_adress) VALUES(?, ?, ?)'
        args = (name, phoneNr, email)
        cursor.execute(query, args)

        id = cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
        return id



        return None

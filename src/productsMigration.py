from src.database import Database


class ProductsMigration:

    def migrate_product_data(self):
        db = Database()

        # db.execute("exec ImportCategoryData")
        # db.execute("exec ImportIngredientData")
        # db.execute("exec ImportSauceData")
        # db.execute("exec ImportCrustData")
        # db.execute("exec ImportPizzaData")

        db.execute("SET NOCOUNT ON exec ImportCategoryData")
        db.execute("SET NOCOUNT ON exec ImportIngredientData")
        db.execute("SET NOCOUNT ON exec ImportSauceData")
        db.execute("SET NOCOUNT ON exec ImportCrustData")
        db.execute("exec ImportPizzaData")


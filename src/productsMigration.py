from src.database import Database
from src.logger import Logger
import pandas as pd
import src
import textwrap

class ProductsMigration:
    def __indent(self, text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

    def migrate_product_data(self):
        db = Database()

        print('Starting products staging table data migration to target')
        db.execute("SET NOCOUNT ON exec ImportCategoryData")
        db.execute("SET NOCOUNT ON exec ImportIngredientData")
        db.execute("SET NOCOUNT ON exec ImportSauceData")
        db.execute("SET NOCOUNT ON exec ImportCrustData")
        db.execute("SET NOCOUNT ON EXEC ImportPizzaData")
        db.execute("SET NOCOUNT ON exec ImportOtherProductData")
        print('products data migration to target done\n')

        engine = src.dbEbgine().get_db_engine()
        try:
            error_dataframe = pd.read_sql("SELECT * FROM product_import_error_log", engine)
            if len(error_dataframe) > 0:
                error_string = "Product migration errors found: \n" \
                               + self.__indent(error_dataframe.to_string(),
                                               30)

                Logger().error(error_string)
        except Exception:
            print("No import errors found")

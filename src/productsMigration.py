import time

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
        start_time = round(time.time() * 1000)

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
                print('Product migration complete with ' + str(len(error_dataframe)) + ' errors in '
                      + str(round(time.time() * 1000) - start_time) + ' seconds. See error logs for details.\n')
                error_string = "Product migration errors found: \n" \
                               + self.__indent(error_dataframe.to_string(),
                                               30)

                Logger().error(error_string)
            else:
                print('Product migration complete with no errors in ' + str(round(time.time() * 1000) - start_time) + 'seconds.\n')
        except Exception:
            print("No import errors found")

        return round(time.time() * 1000) - start_time

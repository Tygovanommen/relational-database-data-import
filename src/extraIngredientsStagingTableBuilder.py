import os
import textwrap
import time

import pandas as pd
import src
from src.logger import Logger
from src.database import Database
from src.price_cleanup_helper import PriceCleanupHelper


class ExtraIngredientsStagingTableBuilder:

    # Constructor to setup extra ingredient importer
    def __init__(self, filename):
        self.filename = filename

    def __indent(self, text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

    def process(self):
        start_time = round(time.time() * 1000)
        print('Building Extra Ingredients Staging Table')
        filepath = os.getcwd() + '/watch/' + self.filename
        cursor = Database().get_connection().cursor()
        if os.path.isfile(filepath):
            engine = src.dbEbgine().get_db_engine()

            ingredienten_date_frame = pd.read_csv(filepath, sep=';')
            PriceCleanupHelper().clean_prices(ingredienten_date_frame, 'Extra Price', self.filename)

            # uniform capitalization of ingredient names.
            ingredienten_date_frame['Ingredient'] = ingredienten_date_frame['Ingredient'].str.title()

            ingredienten_date_frame.to_sql('extra_ingredienten_ghost', con=engine, if_exists='replace')

            cursor.execute("select count(*) from extra_ingredienten_ghost")
            staging_table_count = cursor.fetchone()[0]
            log_string = str(
                'Extra Ingredients staging table done in ' + str(round(time.time() * 1000) - start_time) + ' ms;' + '\n'
                + 'Inserted ' + str(staging_table_count) + ' out of ' + str(
                    len(ingredienten_date_frame.index)) + ' rows into staging table. \n')
            print(log_string)
        return round(time.time() * 1000) - start_time

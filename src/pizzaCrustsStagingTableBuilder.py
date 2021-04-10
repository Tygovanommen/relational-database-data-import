import os
import time

import pandas as pd
import src
from src.database import Database


class PizzaCrustsStagingTableBuilder:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        print('Building Pizza Crusts Staging Table')
        filepath = os.getcwd() + '/watch/' + self.filename
        cursor = Database().get_connection().cursor()
        start_time = round(time.time() * 1000)

        if os.path.isfile(filepath):
            engine = src.dbEbgine().get_db_engine()

            pizza_bodems_data_frame = pd.read_excel(filepath)

            pizza_bodems_data_frame.to_sql('pizza_bodems_ghost', con=engine, if_exists='replace')

            cursor.execute("select count(*) from pizza_bodems_ghost")
            staging_table_count = cursor.fetchone()[0]
            log_string = str(
                'Pizza crusts staging table done in ' + str(round(time.time() * 1000) - start_time) + ' ms;' + '\n'
                + 'Inserted ' + str(staging_table_count) + ' out of ' + str(
                    len(pizza_bodems_data_frame.index)) + ' rows into staging table. \n')
            print(log_string)
        return round(time.time() * 1000) - start_time


import os

import pandas as pd
import src


class PizzaCrustsStagingTableBuilder:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        filepath = os.getcwd() + '/watch/' + self.filename
        if os.path.isfile(filepath):
            engine = src.dbEbgine().get_db_engine()

            pizza_bodems_data_frame = pd.read_excel(filepath)

            pizza_bodems_data_frame.to_sql('pizza_bodems_ghost', con=engine, if_exists='replace')

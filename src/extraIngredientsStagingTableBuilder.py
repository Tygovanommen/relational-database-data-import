import os
import textwrap

import pandas as pd
import src
from src.logger import Logger
from src.price_cleanup_helper import PriceCleanupHelper


class ExtraIngredientsStagingTableBuilder:

    # Constructor to setup extra ingredient importer
    def __init__(self, filename):
        self.filename = filename

    def __indent(self, text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

    def process(self):
        print('Building Extra Ingredients Staging Table')
        filepath = os.getcwd() + '/watch/' + self.filename
        if os.path.isfile(filepath):
            engine = src.dbEbgine().get_db_engine()

            ingredienten_date_frame = pd.read_csv(filepath, sep=';')
            PriceCleanupHelper().clean_prices(ingredienten_date_frame, 'Extra Price', self.filename)

            # uniform capitalization of ingredient names.
            ingredienten_date_frame['Ingredient'] = ingredienten_date_frame['Ingredient'].str.title()

            ingredienten_date_frame.to_sql('extra_ingredienten_ghost', con=engine, if_exists='replace')
            print('Extra Ingredients staging table done\n')

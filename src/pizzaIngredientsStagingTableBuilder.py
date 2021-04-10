import os
import time

import pandas as pd
import src
from src.dataFrameStringCompare import DataFrameStringCompare
from src.database import Database
from src.logger import Logger


class PizzaIngredientsStagingTableBuilder:

    # Constructor to setup shop importer
    def __init__(self, extra_ingredients_filename, pizza_ingredients_filename):
        self.extra_ingredients_filename = extra_ingredients_filename
        self.pizza_ingredients_filename = pizza_ingredients_filename
        self.clean_ingredients_data = True

    def process(self):
        return self.__create_staging_stable()


    def __create_staging_stable(self):
        filepath = os.getcwd() + '/watch/' + self.extra_ingredients_filename
        cursor = Database().get_connection().cursor()
        start_time = round(time.time() * 1000)

        if os.path.isfile(filepath):
            print('Building Pizza Ingredients Staging Table')
            engine = src.dbEbgine().get_db_engine()
            pizza_ingredienten_data_frame = pd.read_excel(filepath)
            pizza_ingredienten_data_frame = pizza_ingredienten_data_frame.loc[:,
                                            ~pizza_ingredienten_data_frame.columns.str.contains('^Unnamed')]

            # uniform capitalization of ingredient names.
            pizza_ingredienten_data_frame['ingredientnaam'] = pizza_ingredienten_data_frame['ingredientnaam'].str.title()

            if self.clean_ingredients_data:
                filepath = os.getcwd() + '/watch/' + self.pizza_ingredients_filename
                ingredienten_date_frame = pd.read_csv(filepath, sep=';')
                ingredienten_date_frame['Ingredient'] = ingredienten_date_frame['Ingredient'].str.title()

                error_message = DataFrameStringCompare(90, pizza_ingredienten_data_frame, 'ingredientnaam', ingredienten_date_frame, 'Ingredient').compare_replace_dataframe_string()
                if(error_message is not None):
                    error_message = error_message + " from dataset: " + self.pizza_ingredients_filename + ". control dataset: " + self.extra_ingredients_filename
                    Logger().error(error_message)


            # TODO: make own helper class.
            pizza_ingredienten_data_frame['spicy'] = pizza_ingredienten_data_frame['spicy'].str.replace('Ja', '1')
            pizza_ingredienten_data_frame['spicy'] = pizza_ingredienten_data_frame['spicy'].str.replace('Nee', '0')
            pizza_ingredienten_data_frame['vegetarisch'] = pizza_ingredienten_data_frame['vegetarisch'].str.replace('Ja',
                                                                                                                    '1')
            pizza_ingredienten_data_frame['vegetarisch'] = pizza_ingredienten_data_frame['vegetarisch'].str.replace('Nee',
                                                                                                                    '0')
            pizza_ingredienten_data_frame["spicy"] = pd.to_numeric(pizza_ingredienten_data_frame["spicy"])
            pizza_ingredienten_data_frame["vegetarisch"] = pd.to_numeric(pizza_ingredienten_data_frame["vegetarisch"])
            pizza_ingredienten_data_frame['spicy'] = pizza_ingredienten_data_frame['spicy'].astype('bool')
            pizza_ingredienten_data_frame['vegetarisch'] = pizza_ingredienten_data_frame['vegetarisch'].astype('bool')

            pizza_ingredienten_data_frame.to_sql('pizza_ingredienten_ghost', con=engine, if_exists='replace')

            cursor.execute("select count(*) from pizza_ingredienten_ghost")
            staging_table_count = cursor.fetchone()[0]
            log_string = str(
                'Pizza ingredients staging table done in ' + str(round(time.time() * 1000) - start_time) + ' ms;' + '\n'
                + 'Inserted ' + str(staging_table_count) + ' out of ' + str(
                    len(pizza_ingredienten_data_frame.index)) + ' rows into staging table. \n')
            print(log_string)
        return round(time.time() * 1000) - start_time



import pandas as pd
import src

# Filename + extension
filename = None



class PizzaIngredientsStagingTableBuilder:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        self.__create_staging_stable()

    def __create_staging_stable(self):
        engine = src.dbEbgine.get_db_engine()
        pizza_ingredienten_data_frame = pd.read_excel("watch/" + self.filename)
        pizza_ingredienten_data_frame = pizza_ingredienten_data_frame.loc[:,
                                        ~pizza_ingredienten_data_frame.columns.str.contains('^Unnamed')]

        # uniform capitalization of ingredient names.
        pizza_ingredienten_data_frame['ingredientnaam'] = pizza_ingredienten_data_frame['ingredientnaam'].str.title()
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

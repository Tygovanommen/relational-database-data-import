import pandas as pd
import src

# Filename + extension
filename = None


class PizzaIngredients:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        engine = src.dbEbgine.get_db_engine()

        pizza_ingredienten_data_frame = pd.read_excel("watch/" + self.filename)
        pizza_ingredienten_data_frame = pizza_ingredienten_data_frame.loc[:, ~pizza_ingredienten_data_frame.columns.str.contains('^Unnamed')]

        # uniform capitalization of ingredient names.
        pizza_ingredienten_data_frame['ingredientnaam'] = pizza_ingredienten_data_frame['ingredientnaam'].str.title()
        pizza_ingredienten_data_frame.to_sql('pizza_ingredienten_ghost', con=engine, if_exists='replace')

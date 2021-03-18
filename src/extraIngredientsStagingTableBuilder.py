import pandas as pd
import src

# Filename + extension
filename = None


class ExtraIngredientsStagingTableBuilder:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        engine = src.dbEbgine.get_db_engine()

        ingredienten_date_frame = pd.read_csv("watch/" + self.filename, sep=';')

        ingredienten_date_frame['Extra Price'] = ingredienten_date_frame['Extra Price'].str.replace(r"[a-zA-Z€ ]", '', regex=True)
        ingredienten_date_frame["Extra Price"] = pd.to_numeric(ingredienten_date_frame["Extra Price"])
        # uniform capitalization of ingredient names.
        ingredienten_date_frame['Ingredient'] = ingredienten_date_frame['Ingredient'].str.title()

        ingredienten_date_frame.to_sql('extra_ingredienten_ghost', con=engine, if_exists='replace')


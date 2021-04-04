import os
import pandas as pd
import src


class OtherProductsStagingTableBuilder:

    # Constructor to setup shop importer
    def __init__(self, filename):
        self.filename = filename

    def process(self):
        print('Building Other Products Staging Table')
        filepath = os.getcwd() + '/watch/' + self.filename
        if os.path.isfile(filepath):
            engine = src.dbEbgine().get_db_engine()

            other_prducts_data_frame = pd.read_excel(filepath)

            other_prducts_data_frame['spicy'] = other_prducts_data_frame['spicy'].str.replace('Ja', '1')
            other_prducts_data_frame['spicy'] = other_prducts_data_frame['spicy'].str.replace('Nee', '0')
            other_prducts_data_frame['vegetarisch'] = other_prducts_data_frame['vegetarisch'].str.replace('Ja',
                                                                                                                    '1')
            other_prducts_data_frame['vegetarisch'] = other_prducts_data_frame['vegetarisch'].str.replace('Nee',
                                                                                                                    '0')
            other_prducts_data_frame["spicy"] = pd.to_numeric(other_prducts_data_frame["spicy"])
            other_prducts_data_frame["vegetarisch"] = pd.to_numeric(other_prducts_data_frame["vegetarisch"])
            other_prducts_data_frame['spicy'] = other_prducts_data_frame['spicy'].astype('bool')
            other_prducts_data_frame['vegetarisch'] = other_prducts_data_frame['vegetarisch'].astype('bool')

            other_prducts_data_frame.to_sql('overige_producten_ghost', con=engine, if_exists='replace')
            print('Other Products Staging Table done\n')
import os
import shutil

from src.logger import Logger
from src.shop import Shop
from src.pizzaIngredientsStagingTableBuilder import PizzaIngredientsStagingTableBuilder
from src.extraIngredientsStagingTableBuilder import ExtraIngredientsStagingTableBuilder
from src.pizzaCrustsStagingTableBuilder import PizzaCrustsStagingTableBuilder
from src.productsMigration import ProductsMigration
from src.zipcode import ZipCode
from src.muncipality import Muncipality
from src.otherProductsStagingTableBuilder import OtherProductsStagingTableBuilder


def main():
    # Loop through 'watch' directory
    files = os.listdir("watch")
    if files:

        # Start processing
        PizzaIngredientsStagingTableBuilder('pizza_ingredienten.xlsx', 'Extra Ingredienten.csv').process()
        ExtraIngredientsStagingTableBuilder('Extra Ingredienten.csv').process()
        PizzaCrustsStagingTableBuilder('pizzabodems.xlsx').process()
        OtherProductsStagingTableBuilder('Overige Producten.xlsx').process()
        ProductsMigration().migrate_product_data()
        Muncipality("Postcode tabel.mdb").process()
        ZipCode("Postcode tabel.mdb").process()
        Shop("Winkels Mario.txt").process()

        # # Move files to 'complete' directory
        # for file in files:
        #     move_file(file)


        Logger().commit_errors()
        # Logger().info("Import completed")


# Move file from watch to complete directory
def move_file(filename):
    dir_from = os.getcwd() + "/watch/" + filename
    dir_to = os.getcwd() + "/complete/" + filename
    shutil.move(dir_from, dir_to)


# Start script
if __name__ == "__main__":
    main()

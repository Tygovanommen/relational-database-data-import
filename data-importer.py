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


def main():
    # Loop through 'watch' directory
    files = os.listdir("watch")
    if files:
        Logger().info("Import started")

        # Start processing
        PizzaIngredientsStagingTableBuilder('pizza_ingredienten.xlsx').process()
        ExtraIngredientsStagingTableBuilder('Extra Ingredienten.csv').process()
        PizzaCrustsStagingTableBuilder('pizzabodems.xlsx').process()
        ProductsMigration().migrate_product_data()
        Muncipality("Postcode tabel.mdb").process()
        ZipCode("Postcode tabel.mdb").process()
        Shop("Winkels Mario.txt").process()

        Logger().info("Import complete")
    else:
        Logger().info("No files found to import")


# Move file from watch to complete directory
def move_file(filename):
    shutil.move(os.getcwd() + "/watch/" + filename, os.getcwd() + "/complete/" + filename)


# Start script
if __name__ == "__main__":
    main()

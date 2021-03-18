import os
import shutil

from src.logger import Logger
from src.shop import Shop
from src.pizzaIngredientsStagingTableBuilder import PizzaIngredientsStagingTableBuilder
from src.extraIngredientsStagingTableBuilder import ExtraIngredientsStagingTableBuilder
from src.pizzaCrustsStagingTableBuilder import PizzaCrustsStagingTableBuilder
from src.productsMigration import ProductsMigration


def main():
    log = Logger()

    # Loop through 'watch' directory
    files = os.listdir("watch")

    PizzaIngredientsStagingTableBuilder('pizza_ingredienten.xlsx').process()
    ExtraIngredientsStagingTableBuilder('Extra Ingredienten.csv').process()
    PizzaCrustsStagingTableBuilder('pizzabodems.xlsx').process()
    ProductsMigration().migrate_product_data()


    if files:
        log.info("Import started")

        # Step by step process files
        # if Shop("Winkels Mario.txt").process():
        #     print("Done")
        #
        #     move_file("Winkels Mario.txt")
        #     # TBD next file

        log.info("Import complete")
    else:
        log.info("No files found to import")


# Move file from watch to complete directory
def move_file(filename):
    shutil.move(os.getcwd() + "/watch/" + filename, os.getcwd() + "/complete/" + filename)


# Start script
if __name__ == "__main__":
    main()

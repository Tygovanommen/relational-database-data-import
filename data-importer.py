import os
import shutil

from src.OrderData import OrderData
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
        run_time = PizzaIngredientsStagingTableBuilder('pizza_ingredienten.xlsx', 'Extra Ingredienten.csv').process()
        run_time += ExtraIngredientsStagingTableBuilder('Extra Ingredienten.csv').process()
        run_time += PizzaCrustsStagingTableBuilder('pizzabodems.xlsx').process()
        run_time += OtherProductsStagingTableBuilder('Overige Producten.xlsx').process()

        print('All staging tables built in ' + str(run_time) + ' ms. \n')

        run_time += ProductsMigration().migrate_product_data()

        print('Product data migrated in ' + str(run_time) + ' milliseconds.\n')

        Muncipality("Postcode tabel.mdb").process()
        ZipCode("Postcode tabel.mdb").process()
        Shop("Winkels Mario.txt").process()
        OrderData("MarioOrderData01_10000.csv")
        OrderData("MarioOrderData02_10000.csv")
        OrderData("MarioOrderData03_10000.csv")
        OrderData("MarioOrderData04_10000.csv")
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

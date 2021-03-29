import os
import shutil

from src.Entities import Product
from src.Entities.Restaurant import getStoreByName
from src.OrderData import OrderData
from src.logger import Logger
from src.shop import Shop
from src.pizzaIngredients import PizzaIngredients
from src.extraIngredients import ExtraIngredients
from src.pizzaCrusts import PizzaCrusts
from src.Entities import Restaurant


def main():
    # Loop through 'watch' directory
    files = os.listdir("watch")

    if files:
        Logger().info("Import started")

        # Start processing
        # PizzaIngredients('pizza_ingredienten.xlsx').process()
        # ExtraIngredients('Extra Ingredienten.csv').process()
        # PizzaCrusts('pizzabodems.xlsx').process()
        #Shop("Winkels Mario.txt").process()
        OrderData('MarioOrderData02_10000.csv').process()

        Logger().info("Import complete")
    else:
        Logger().info("No files found to import")


# Move file from watch to complete directory
def move_file(filename):
    shutil.move(os.getcwd() + "/watch/" + filename, os.getcwd() + "/complete/" + filename)


# Start script
if __name__ == "__main__":
    main()



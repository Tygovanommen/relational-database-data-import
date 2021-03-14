import os
import shutil

from src.logger import Logger
from src.shop import Shop
from src.pizzaIngredients import PizzaIngredients
from src.extraIngredients import ExtraIngredients
from src.pizzaCrusts import PizzaCrusts


def main():
    log = Logger()

    # Loop through 'watch' directory
    files = os.listdir("watch")

    PizzaIngredients('pizza_ingredienten.xlsx').process()
    ExtraIngredients('Extra Ingredienten.csv').process()
    PizzaCrusts('pizzabodems.xlsx').process()

    if files:
        log.info("Import started")

        # Step by step process files
        if Shop("Winkels Mario.txt").process():
            print("Done")

            move_file("Winkels Mario.txt")
            # TBD next file

        log.info("Import complete")
    else:
        log.info("No files found to import")


# Move file from watch to complete directory
def move_file(filename):
    shutil.move(os.getcwd() + "/watch/" + filename, os.getcwd() + "/complete/" + filename)


# Start script
if __name__ == "__main__":
    main()

import os
import shutil

from src.logger import Logger
from src.shop import Shop


def main():
    log = Logger()

    # Loop through 'watch' directory
    files = os.listdir("watch")
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

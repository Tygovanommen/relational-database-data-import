import configparser
import os


class ConfigParser:

    def __init__(self):
        # Parse file
        config = configparser.ConfigParser()
        config.read(os.getcwd() + "/config.ini")

        # Create array with config values
        self.values = {}
        self.values["Server"] = config.get('database', 'Server')
        self.values["Database"] = config.get('database', 'Database')
        self.values["Username"] = config.get('database', 'Username')
        self.values["Password"] = config.get('database', 'Password')

    # Get config values
    def get_config(self):
        return self.values

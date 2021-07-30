import os
import json


class ConfigReader:
    def __init__(self):
        self.config = None

    def read_config(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        with open(os.path.join(__location__, 'config.json')) as f:
            data = json.load(f)

        self.config = data

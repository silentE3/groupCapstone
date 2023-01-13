'''config holds the logic to read in a configuration object'''
import json
from app.models import Configuration


def read_json(config_path: str) -> Configuration:
    """Reads in a json configuration file"""
    with open(config_path, mode="r", encoding="UTF-8") as json_file:
        data: Configuration = json.load(json_file)

# The following global module variables and assignments are a move towards
# creating a single instance of the configuration that does not need to be
# passed to each method.
    #pylint: disable=global-statement
    global CONFIG_DATA
    CONFIG_DATA = data

    return data


CONFIG_DATA = None

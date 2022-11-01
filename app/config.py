'''config holds the logic to read in a configuration object'''
import json
from app.models import Configuration


def read_json(config_path: str) -> Configuration:
    """Reads in a json configuration file"""
    with open(config_path, mode="r", encoding="UTF-8") as json_file:
        data: Configuration = json.load(json_file)

        return data

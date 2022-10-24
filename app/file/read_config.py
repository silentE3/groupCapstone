"""This will read in the config data, expected in json format"""
import json
from typing import cast
from app.data_classes import config


def read_config_json(config_path: str) -> config.GroupingConfig:
    """Reads in a json file containing the configuration data for this run of grouping"""
    with open(config_path, mode="r", encoding="UTF-8") as json_file:
        data = json.load(json_file)

        return cast(config.GroupingConfig, data)

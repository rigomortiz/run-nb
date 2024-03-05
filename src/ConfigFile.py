import csv
import sys
import os
import configparser
import logging
from typing import Any
from src import Constants


class ConfigFile:
    @staticmethod
    def read(file: str) -> dict[Any, Any]:
        """
        Read config file
        :param file: Path to config file
        :return: dict with config
        """
        try:
            if not os.path.exists(file):
                logging.error(f'Path {file} not exists')
                sys.exit(1)
            conf = configparser.ConfigParser()
            conf.read(file)
            config_dict = dict()
            sections = conf.sections()
            for section in sections:
                if conf.has_option(section, Constants.PARAMS + Constants.POINT + Constants.FILE):
                    params_dict = {Constants.PARAMS: []}
                    params_file = conf.get(section, Constants.PARAMS + Constants.POINT + Constants.FILE)
                    reader = csv.DictReader(open(params_file))
                    for row in reader:
                        params_dict[Constants.PARAMS].append(row)
                elif conf.has_option(section, Constants.PARAMS):
                    params = conf.get(section, Constants.PARAMS).split(Constants.COME)
                    params_array = []
                    for param in params:
                        params_array.append({Constants.PARAM: param})
                    params_dict = {Constants.PARAMS: params_array}
                else:
                    params_dict = {Constants.PARAMS: [{'PARAM': ''}]}
                if not conf.has_option(section, Constants.NOTEBOOKS):
                    logging.error(f'Not found notebooks in section {section}')
                    continue
                else:
                    notebooks = conf.get(section, Constants.NOTEBOOKS).split(Constants.COME)
                    config_dict[section] = params_dict | {Constants.NOTEBOOKS: notebooks}

                if conf.has_option(section, Constants.KERNEL):
                    config_dict[section] = config_dict[section] | {
                        Constants.KERNEL: conf.get(section, Constants.KERNEL)
                    }
                else:
                    config_dict[section] = config_dict[section] | {Constants.KERNEL: Constants.PYTHON3}

                if conf.has_option(section, Constants.SAVE) and (conf.get(section, Constants.SAVE) == 'False'
                                                                 or conf.get(section, Constants.SAVE) == 'false'):
                    config_dict[section] = config_dict[section] | {Constants.SAVE: False}
                else:
                    config_dict[section] = config_dict[section] | {Constants.SAVE: True}
            logging.info('Config file read successfully')
            logging.info(config_dict)
            return config_dict
        except configparser.Error as e:
            logging.error(f'Not open config file: {e}')
            sys.exit(1)
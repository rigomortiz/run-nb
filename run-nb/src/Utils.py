import json
import logging
import os
import numpy as np
import nbformat
from src import Constants
class Utils:
    @staticmethod
    def read_config_file(file_path: str) -> dict or None:
        try:
            file = open(file_path)
            return json.load(file)
        except FileNotFoundError:
            return None
    @staticmethod
    def read_env_file(file_path: str) -> dict or None:
        try:
            file = open(file_path)
            args = dict()
            for line in file:
                key, value = line.split('=')
                args[key] = value.replace('\n', '')
                os.environ[key] = value.replace('\n', '')
            return args
        except FileNotFoundError:
            return None
    @staticmethod
    def write_params_to_notebook(params):
        with open(Constants.INPUT_PATH + os.sep + Constants.ENV_FILE, Constants.MODE) as file:
            for param in params:
                file.write(param + '\n')

    @staticmethod
    def get_env() -> dict:
        return os.environ.copy()

    @staticmethod
    def set_env(params: list) -> None:
        for param in params:
            os.environ[param[Constants.NAME]] = param[Constants.VALUE]

    @staticmethod
    def clean_env() -> None:
        os.environ.clear()

    @staticmethod
    def create_directories(folder) -> None:
        if not os.path.exists(Constants.OUTPUT):
            os.makedirs(Constants.OUTPUT)
        if not os.path.exists(Constants.OUTPUT + os.sep + folder):
            os.makedirs(Constants.OUTPUT + os.sep + folder)

    @staticmethod
    def get_cell_read_env() -> nbformat.notebooknode.NotebookNode:
        source = '''
import os
file = open('.env')
args = dict()
for line in file:
    key, value = line.split('=')
    args[key] = value.replace('\\n', '')
    os.environ[key] = value.replace('\\n', '')
                    '''
        return nbformat.v4.new_code_cell(source)

    @staticmethod
    def end_cell() -> nbformat.notebooknode.NotebookNode:
        source = '''
import os
with open(PATH + os.path.sep + 'variables.env', 'w') as file:
    print('Saving .env ...')
    vs = [[x.replace('@', ''), os.environ[x]] for x in list(os.environ.copy().keys()) if x[0] == '@' and x[-1] == '@']
    for v in vs:
        file.write(v[0] + '=' + v[1] + "\\n")
    '''
        return nbformat.v4.new_code_cell(source)

    @staticmethod
    def start_cell(params) -> nbformat.notebooknode.NotebookNode:
        ps = "# Variables Globales\n"
        ps += ''.join([key + ' = \'' + params[key] + '\'\n' for key in params])
        with open('run-nb/src/TestMagic.py') as file:
            source = file.read()

        return nbformat.v4.new_code_cell(ps + source)

    @staticmethod
    def merge_notebooks(paths, path_output):
        cells = []
        for p in paths:
            with open(p, 'r') as file:
                cells.append(json.loads(file.read())['cells'])
        with open(paths[0], 'r') as file:
            new_dict = json.loads(file.read()).copy()
            new_dict['cells'] = list(np.concatenate(cells))
        with open(path_output, 'w') as json_file:
            json.dump(new_dict, json_file)
        return True

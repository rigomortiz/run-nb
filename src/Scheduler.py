import logging
import os.path
import os

from src.Notebook import Notebook
from src import Constants
class Scheduler:
    """
    Constructor
    """
    def __init__(self, notebooks: dict, path: str, project_name: str = 'notebooks'):
        logging.info('Initializer scheduler ...')
        self.notebooks = []
        project_output_path = path + os.path.sep + Constants.OUTPUT + os.path.sep + project_name
        if not os.path.exists(project_output_path):
            logging.info(f'Path  {project_output_path} not exists, creating ...')
            os.makedirs(project_output_path)
        keys = notebooks.keys()
        logging.info(f'Numero de notebooks: {len(keys)}')
        for key in keys:
            logging.info(f'Notebook: {key}')
            path = notebooks.get(key).get(Constants.NOTEBOOKS)[0]
            params = notebooks.get(key).get(Constants.PARAMS)
            i = 1
            for param in params:
                logging.info(f'Parametros: {param}')
                output_path = ''
                if Constants.CARPETA in param:
                    output_path = project_output_path + os.path.sep + key + os.path.sep + param[
                        Constants.CARPETA] + os.path.sep
                elif Constants.PARAM in param and param[Constants.PARAM] != '':
                    output_path = project_output_path + os.path.sep + key + os.path.sep + param[
                        Constants.PARAM] + os.path.sep
                elif Constants.PARAM in param and param[Constants.PARAM] == '':
                    output_path = project_output_path + os.path.sep + key + os.path.sep
                else:
                    output_path = project_output_path + os.path.sep + key + os.path.sep + str(i) + os.path.sep
                    i += 1

                if not os.path.exists(output_path):
                     logging.info(f'Path  {output_path} not exists, creating ...')
                     os.makedirs(output_path)

                logging.info(f'Inicializando notebook {path} ...')
                param[Constants.OUTPUT_PATH] = output_path
                param[Constants.CARPETA] = param[Constants.OUTPUT_PATH].split(os.path.sep)[-2]
                nb = Notebook(path=path, params=param, kernel_name=notebooks.get(key).get(Constants.KERNEL))
                self.notebooks.append(nb)
    def get_notebooks(self) -> list[Notebook]:
        return self.notebooks
    def run(self) -> None:
        logging.info('Running notebooks...')
        self.__run_notebooks()
        logging.info('Done')
    def __run_notebooks(self) -> None:
        for i in range(len(self.notebooks)):
            #Utils.set_env(self.notebooks[i].params)
            logging.info('Running notebook number: %s of %s', str(i + 1), str(len(self.notebooks)))
            logging.info('Running notebook: %s', self.notebooks[i].path)
            logging.info('Params: %s', str(self.notebooks[i].params))
            self.notebooks[i].run()

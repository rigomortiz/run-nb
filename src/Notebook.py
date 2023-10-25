import logging
import os
import nbformat
from nbclient.exceptions import CellExecutionError
from nbconvert.preprocessors import ExecutePreprocessor
from src.Utils import Utils
from src import Constants

class Notebook:
    def __init__(self, path: str, params: dict, kernel_name: str = Constants.PYTHON3):
        self.path = path
        self.params = params
        self.kernel_name = kernel_name

    def __str__(self):
        return 'path=' + self.path + ', params=' + str(self.params) + ', kernel_name=' + self.kernel_name

    def run(self) -> None:
        logging.info(f'Open file: {self.path}')
        with open(self.path) as f:
            nb = nbformat.read(f, as_version=Constants.AS_VERSION)
            name = os.path.basename(self.path)
            path = self.params[Constants.OUTPUT_PATH] + name
            logging.info(f'Notebook: {name} version: {Constants.AS_VERSION} running with kernel {self.kernel_name}')
            logging.info('Running cells...')
            # Add cell to init
            nb.cells.insert(0, Utils.start_cell(self.params))
            # Add cell to save env variables
            #nb.cells.insert(len(nb.cells) + 1, Utils.end_cell())
            ep = ExecutePreprocessor(timeout=Constants.TIMEOUT, kernel_name=self.kernel_name, startup_timeout=Constants.STARTUP_TIMEOUT)
            try:
                out = ep.preprocess(nb, {})
                #logging.info('NOTEBOOK\n\n %s', out)
                logging.info(f'Notebook: {name} executed successfully')
                logging.info(f'Saving notebook: {path}')
            except CellExecutionError:
                out = None
                logging.error(f'Error executing the notebook \'{name}\'.\n\n See notebook \'{path}\' for the traceback.')
                raise
            finally:
                with open(path, mode=Constants.MODE, encoding=Constants.UTF_8) as fnb:
                    nbformat.write(nb, fnb, version=Constants.AS_VERSION)

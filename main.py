import os
import logging
import sys
from datetime import datetime
from src import Constants
from src.ConfigFile import ConfigFile
from src.Scheduler import Scheduler

def log_config():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    fh = logging.FileHandler(Constants.LOG_FILE_NAME + '_' + datetime.now().strftime(Constants.FORMAT_DATE) + Constants.LOG_FILE_EXTENSION)
    fh.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[fh, sh])

if __name__ == '__main__':
    log_config()
    logging.info(os.path.dirname(os.path.realpath(__file__)))
    if len(sys.argv) < 2:
        logging.error('Not found config file')
        sys.exit(1)

    for i in range(1, len(sys.argv)):
        logging.info(f'Config file: {sys.argv[i]}')
        if not os.path.exists(sys.argv[i]):
            logging.error(f'Path {sys.argv[i]} not exists')
            continue

        project_name = sys.argv[i].split(Constants.SLASH)[-1].split(Constants.POINT)[0]
        path = '/'.join(sys.argv[i].split(Constants.SLASH)[0:-1])
        logging.info(f'Project name: {project_name}')
        logging.info(f'Path: {path}')
        config = ConfigFile.read(sys.argv[i])
        scheduler = Scheduler(config, path, project_name)
        scheduler.run()

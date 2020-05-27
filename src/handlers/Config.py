from sys import argv
import logging
from wx import DefaultPosition
from logging.handlers import RotatingFileHandler
from pathlib import Path
from configobj import ConfigObj, ConfigObjError

from helpers import DazHelpers

MB_SCALAR = 1024 * 1024


class ConfigHandler:

    def __init__(self):
        self.user_folder_path: Path = DazHelpers.get_adi_user_folder()
        self.debug = True if '--debug' in argv else False

        if not self.user_folder_path.exists():
            self.user_folder_path.mkdir(parents=True)

        self._init_logger()

        self.config_path = self.user_folder_path / 'config.ini'
        self.import_script_path = self.user_folder_path / 'import.dsa'
        self.critical = False

        if not self.config_path.exists(): self._create_config()

        try:
            self._config: ConfigObj = ConfigObj(str(self.config_path), encoding='utf-8')
        except ConfigObjError as e:
            logging.critical('Error when establishing connection to ini file')
            logging.critical(e)
            self._config = None
            self.critical = True
            return

        # load Options
        self.expand: bool = bool(self._config['Options']['expand'])
        self.close_dialog: bool = bool(self._config['Options']['close_dialog'])
        self.detect: bool = bool(self._config['Options']['detect'])

        # load Directories
        self.sources: dict = self._config['Sources']
        self.libraries: dict = self._config['Libraries']

        # load Dimensions
        self.win_size = list(map(int, self._config['Dimensions']['win_size']))
        self.win_pos = list(map(int, self._config['Dimensions']['win_pos']))
        self.first = bool(self._config['Dimensions']['first'])
        self.version = self._config['Dimensions']['version']

    def _create_config(self):
        self._config = ConfigObj()
        self._config.filename = self.config_path

        self._config['Options'] = {}
        self._config['Options']['expand'] = True
        self._config['Options']['close_dialog'] = False
        self._config['Options']['detect'] = False

        self._config['Sources'] = {}
        self._config['Sources']['default_archive'] = DazHelpers.get_default_archive_path()

        self._config['Libraries'] = {}
        self._config['Libraries']['default_library'] = DazHelpers.get_default_library_path()

        self._config['Dimensions'] = {}
        self._config['Dimensions']['win_size'] = (1300, 800)
        self._config['Dimensions']['win_pos'] = DefaultPosition.Get()
        self._config['Dimensions']['first'] = True
        self._config['Dimensions']['version'] = 'temp'

        logging.info(f'Creating {self.config_path.name} in {self.user_folder_path}')
        self._config.write()

    def save_config(self, position=None, size=None):
        self._config['Sources'] = self.sources
        self._config['Libraries'] = self.libraries

        self._config['Options'] = {}
        self._config['Options']['expand'] = self.expand
        self._config['Options']['close_dialog'] = self.close_dialog
        self._config['Options']['detect'] = self.detect

        self._config['Dimensions'] = {}
        if size is not None:
            logging.debug('Setting win_size to: ' + str(size))
            self._config['Dimensions']['win_size'] = size
        if position is not None:
            logging.debug('Setting win_pos to: ' + str(position))
            self._config['Dimensions']['win_pos'] = position
        self._config['Dimensions']['first'] = self.first
        self._config['Dimensions']['version'] = self.version

        logging.debug('Saving config to: ' + str(self.config_path.name))
        self._config.write()

    def _init_logger(self, max_size: int = 2):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        debug_handler = RotatingFileHandler(str(self.user_folder_path / 'log_debug.txt'),
                                            mode='a', maxBytes=max_size * MB_SCALAR,
                                            backupCount=1, encoding='utf-8', delay=False)

        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)

        info_handler = RotatingFileHandler(str(self.user_folder_path / 'log.txt'),
                                           mode='a', maxBytes=max_size * MB_SCALAR,
                                           backupCount=1, encoding='utf-8', delay=False)

        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)

        level = logging.DEBUG if self.debug else logging.INFO
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logging.debug('Logger initialized')

# DBHandler.py
import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from helpers import DazHelpers

from mySQL.AlchTables import Base


class DBHandler:

    def __init__(self, filename: str = 'adi.db'):
        self.path: Path = DazHelpers.get_adi_user_folder() / filename
        self.engine = create_engine(f'sqlite:///{self.path}')

        if not self.path.exists():
            Base.metadata.create_all(self.engine)
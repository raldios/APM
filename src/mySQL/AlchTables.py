import logging
from pathlib import Path
from sqlite3 import Error as sqlError

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker

from helpers import FileHelpers

Base = declarative_base()


class Asset(Base):

    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)

    sku = Column(Integer)
    product_name = Column(String)
    filename = Column(String, unique=True)

    path_raw = Column(String)
    size_raw = Column(Integer)
    installed_raw = Column(Boolean)

    def __repr__(self):
        return f'asset entry: {self.product_name}'

    @property
    def path(self):
        return Path(self.path_raw)

    @property
    def size(self, places=2):
        return FileHelpers.format_bytes(self.size_raw, places)

    @property
    def installed(self):
        text = 'Not' if not self.installed_raw else 'Installed'
        return text


class Folder(Base):

    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True, unique=True)
    path_raw = Column(String, unique=True)
    file_count = Column(Integer)
    size_raw = Column(Integer)

    def __repr__(self):
        return f'folder entry: {self.path}'

    @property
    def path(self):
        return Path(self.path_raw)

    @property
    def size(self, places=2):
        return FileHelpers.format_bytes(self.size_raw, places)

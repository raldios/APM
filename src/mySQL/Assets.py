# Assets.py
import logging
from pathlib import Path

from sqlalchemy.orm import sessionmaker, Session

from mySQL.AlchTables import Asset
from mySQL.DBHandler import DBHandler
from helpers import FileHelpers, SQLHelpers, DazHelpers


class Assets:

    def __init__(self):
        self.db = DBHandler()

    @property
    def all(self):
        session: Session = sessionmaker(bind=self.db.engine, expire_on_commit=False)()
        return session.query(Asset).all()

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.db.engine, expire_on_commit=False)()
        return session.query(Asset).filter_by(*args, **kwargs)

    def create(self, path: Path, source_id: int):

        if path.suffix != '.zip':
            logging.critical('Path provided does not point to a zip file')
            return None

        asset = self.filter_by(filename=str(path.name)).first()  # check if asset already exists in db

        if asset is None:
            sku = DazHelpers.get_sku(path)
            product_name = DazHelpers.parse_product_name(path)
            path_raw = str(path)
            filename = path.name
            size_raw = FileHelpers.get_file_size(path)
            installed_raw = False  # todo check if asset is already installed
            imported_raw = False

            asset = Asset(source_id=source_id,
                          sku=sku,
                          product_name=product_name,
                          path_raw=path_raw,
                          filename=filename,
                          size_raw=size_raw,
                          installed_raw=installed_raw,
                          imported_raw=imported_raw)

            session: Session = sessionmaker(bind=self.db.engine, expire_on_commit=False)()
            SQLHelpers.commit(session, asset)

        return asset

    def update(self, asset_id: int, **kwargs):
        session: Session = sessionmaker(bind=self.db.engine)()
        asset = session.query(Asset).filter_by(id=asset_id).first()

        for key, val in kwargs.items():
            setattr(asset, key, val)

        SQLHelpers.commit(session)
# Folders.py
import logging
from pathlib import Path

from sqlalchemy.orm import sessionmaker, Session

from mySQL.AlchTables import Folder
from mySQL.DBHandler import DBHandler
from helpers import SQLHelpers, FolderHelpers


class Folders:

    def __init__(self):
        self.db = DBHandler()

    def __getitem__(self, folder_id: int):
        session: Session = sessionmaker(bind=self.db.engine, expire_on_commit=False)()
        return session.query(Folder).filter_by(id=folder_id).first()

    def filter_by(self, *args, **kwargs):
        session: Session = sessionmaker(bind=self.db.engine, expire_on_commit=False)()
        return session.query(Folder).filter_by(*args, **kwargs)

    def create(self, path: Path, source_id: int):
        session: Session = sessionmaker(bind=self.db.engine, expire_on_commit=False)()
        folder: Folder = self.filter_by(path_raw=str(path)).first()

        if folder is None:
            title = path.name
            file_count = FolderHelpers.get_zip_count(path)
            size_raw = FolderHelpers.get_folder_size(path)

            folder: Folder = Folder(source_id=source_id, path_raw=str(path), title=title,
                                    file_count=file_count, size_raw=size_raw)

            SQLHelpers.commit(session, folder)

        return folder

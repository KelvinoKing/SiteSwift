#!/user/bin/python3
"""This is the storage for SITESWIFT"""
from os import getenv


storage_t = getenv("SITESWIFT_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()

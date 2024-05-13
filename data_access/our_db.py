from pathlib import Path

from sqlalchemy import create_engine
from data_models.Our_models import *


def init_our_db(database_file):
    database_path = Path(database_file)
    data_folder = database_path.parent
    engine = create_engine(f"sqlite:///{database_path}")
    if database_path.is_file():
        Base.metadata.drop_all(engine)
    else:
        if not data_folder.exists():
            data_folder.mkdir(parents=True)

    Base.metadata.create_all(engine)

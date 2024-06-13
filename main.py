# Python

import os
from pathlib import Path
from sqlalchemy import create_engine
from data_models.models import *

from console.console_base import *
from ui.mainMenu import MainMenu
from data_access.data_base import init_db

DB_DIR = "./data"
DEFAULT_DB_FILE = "hotel_reservation.db"
TEST_DB_FILE = "test_hotel_reservation.db"

DEFAULT_DB = f"sqlite:///{DB_DIR}/{DEFAULT_DB_FILE}"
TEST_DB = f"sqlite:///{DB_DIR}/{TEST_DB_FILE}"

if __name__ == "__main__":
    # Get the DB_FILE environment variable, set to TEST_DB_FILE if not set
    db_file = os.environ.get('DB_FILE', TEST_DB_FILE)

    db_path = Path(os.path.join(DB_DIR, db_file))

    # initialize the database
    init_db(str(db_path.resolve()))

    print("Database tables have been created.")

    # Access to main Menu
    main_menu = MainMenu(db_path)

    # create the application with the very first menu to start
    app = Application(main_menu)

    # run the application which starts with the main menu set in the constructor above
    app.run()


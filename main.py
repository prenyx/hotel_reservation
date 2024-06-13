# Python

import os
from pathlib import Path

from console.console_base import *
from ui.mainMenu import MainMenu
from data_models.models import *

DEFAULT_DB = "./data/hotel_reservation.db"
TEST_DB = "./data/test_hotel_reservation.db"

if __name__ == "__main__":

    # if the environment variable is not set, set it to default
    if not os.environ.get('DB_FILE'):
        os.environ['DB_FILE'] = TEST_DB

    db_path = Path(os.environ.get('DB_FILE'))

    # creates the file if it does not exist
    db_path.touch(exist_ok=True)

    __engine = create_engine(os.environ.get('DB_FILE'))
    metadata.create_all(bind=__engine)  # bind the engine to the metadata of the Base class

    # create the very first main menu
    main_menu = MainMenu(db_path)
    # create the app with the very first menu to start
    app = Application(main_menu)
    # run the app which starts with the main menu set in the constructor above.
    app.run()




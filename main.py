# Python

import os
from pathlib import Path
from sqlalchemy import create_engine
from data_models.models import *

from console.console_base import *
from ui.mainMenu import MainMenu
from data_access.data_base import *


DB_DIR = "./data"
DEFAULT_DB_FILE = "hotel_reservation.db"
TEST_DB_FILE = "test_hotel_reservation.db"

DEFAULT_DB = f"sqlite:///{DB_DIR}/{DEFAULT_DB_FILE}"
TEST_DB = f"sqlite:///{DB_DIR}/{TEST_DB_FILE}"


def main(db_url, db_path):
    """Initialize the database"""
    init_db(db_path)

    engine = create_engine(db_url)
    print('Database initialized')

    # Create a new SQLAlchemy session
    with Session(engine) as session:
        # Check if any data exists in the Role table
        if session.query(Role).first() is None:  # If not, generate data
            generate_system_data(engine, True)

        # Similarly, add checks for each type of data generation
        if session.query(Hotel).first() is None:
            generate_hotels(engine, True)

        if session.query(RegisteredGuest).first() is None:
            generate_registered_guests(engine, True)

        if session.query(Booking).first() is None:
            generate_random_bookings(engine, 100, verbose=True)

        # if session.query(RegisteredBooking).first() is None:
        #     generate_random_registered_bookings(engine, 25, verbose=True)

    # Access to main Menu
    main_menu = MainMenu(db_path)

    # create the application with the very first menu to start
    app = Application(main_menu)

    # Run the application which starts with the main menu set in the constructor above
    app.run()


if __name__ == "__main__":
    db_file = os.environ.get('DB_FILE', TEST_DB_FILE)
    db_path = Path(os.path.join(DB_DIR, db_file)).resolve()
    db_url = "sqlite:///" + str(db_path).replace("\\", "/")

    main(db_url, db_path)





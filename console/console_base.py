import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from business.UserManager import UserManager
from business.HotelManager import HotelManager
from data_access.data_base import init_db
from data_models import models
from data_models.models import Base, Guest, Login
from pathlib import Path


class Console(object):

    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        self._database_path = database_path  # store the database_path as an instance variable

    def run(self):
        raise NotImplementedError("Implement this method")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')


class Application(object):

    def __init__(self, start: Console):
        self._current: Console = start

    def run(self):
        while self._current:
            self._current = self._current.run()


class MenuOption(object):
    def __init__(self, title):
        self._title = title

    def get_title(self) -> str:
        return self._title

    def __str__(self):
        return self._title

    def __len__(self):
        return len(self._title)


class Menu(Console):
    def __init__(self, title, database_path: Path, width=50):
        super().__init__(database_path)
        self._title = title
        self._options = []
        self._width = width

    def __iter__(self):
        return iter(self._options)

    def get_options(self) -> list:
        return self._options

    def add_option(self, option: MenuOption):
        self._options.append(option)

    def remove_option(self, option: MenuOption):
        self._options.remove(option)

    def _show(self):
        print("#" * self._width)
        left = "# "
        right = "#"
        space = " " * (self._width - len(left) - len(self._title) - len(right))
        print(f"{left}{self._title}{space}{right}")
        print("#" * self._width)
        for i, option in enumerate(self, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("#" * self._width)

    def _make_choice(self) -> int:
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            self._show()
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == len(self._options):  # Back or exit
            return StartConsole(self._database_path)
        elif choice == 1:
            return UserRegistrationConsole(self._database_path)
        elif choice == 2:
            return HotelManagementConsole(self._database_path)
        return self

    def run(self) -> Console:
        self.clear()
        self._show()
        return self._navigate(self._make_choice())

class StartConsole(Menu):
    def __init__(self, database_path: Path):
        super().__init__("Main Menu", database_path)
        self.add_option(MenuOption("User Registration"))
        self.add_option(MenuOption("Hotel Management"))
        self.add_option(MenuOption("Exit"))

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            return UserRegistrationConsole(self._database_path)
        elif choice == 2:
            return HotelManagementConsole(self._database_path)
        return None  # Exit
class UserRegistrationConsole(Console):
    def __init__(self, database_path: Path):
        super().__init__(database_path)
        self._user_manager = UserManager(database_path)

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            self.create_new_login()
            return self
        elif choice == 2:
            self.register_existing_user()
            return self
        return StartConsole(self._database_path)  # Back to main menu

    def create_new_login(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return
        self._user_manager.create_new_login(email, password)

    def register_existing_user(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        self._user_manager.register_existing_user(email, password)

    def run(self):
        menu = Menu("Hotel Reservation System", self._database_path)
        menu.add_option(MenuOption("Create New Login"))
        menu.add_option(MenuOption("Register Existing User"))
        menu.add_option(MenuOption("Back to Main Menu"))
        return menu

class HotelManagementConsole(Console):


    def __init__(self, database_path: Path):
        super().__init__(database_path)
        self._hotel_manager = HotelManager(database_path)

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            name = input("Enter hotel name: ")
            address = input("Enter hotel address: ")
            stars = input("Enter hotel stars: ")
            HotelManager.add_hotel(name, address, stars)
        elif choice == 2:
            hotel_id = input("Enter hotel ID to remove: ")
            HotelManager.remove_hotel(hotel_id)
        elif choice == 3:
            hotel_id = input("Enter hotel ID to update: ")
            name = input("Enter new hotel name (or press Enter to skip): ")
            address = input("Enter new hotel address (or press Enter to skip): ")
            stars = input("Enter new hotel stars (or press Enter to skip): ")
            HotelManager.update_hotel_info(hotel_id, name if name else None, address if address else None,
                                           stars if stars else None)
        elif choice == 4:
            HotelManager.view_all_bookings()
        elif choice == 5:
            booking_id = input("Enter booking ID to update: ")
            phone_number = input("Enter new phone number (or press Enter to skip): ")
            HotelManager.edit_booking(booking_id, phone_number if phone_number else None)
        elif choice == 6:
            hotel_id = input("Enter hotel ID: ")
            room_number = input("Enter room number: ")
            available = input("Is the room available? (yes/no): ").lower() == 'yes'
            HotelManager.manage_room_availability(hotel_id, room_number, available)
        elif choice == 7:
            hotel_id = input("Enter hotel ID: ")
            room_number = input("Enter room number: ")
            price = input("Enter new price: ")
            HotelManager.update_room_price(hotel_id, room_number, price)
        elif choice == 8:
            return StartConsole(self._database_path)
        else:
            return Menu("Invalid Option Handled", self._database_path)
        return self

    def run(self):
        menu = Menu("Hotel Reservation System: Hotelmanagement", self._database_path)
        menu.add_option(MenuOption("Add Hotel"))
        menu.add_option(MenuOption("Remove Hotel"))
        menu.add_option(MenuOption("Update Hotel Info"))
        menu.add_option(MenuOption("View All Bookings"))
        menu.add_option(MenuOption("Manage Room Availability"))
        menu.add_option(MenuOption("Manage Room Price"))
        menu.add_option(MenuOption("Back to Main Menu"))
        return menu
if __name__ == "__main__":
    database_path = Path("../data/my_db.db")
    app = Application(StartConsole(database_path))
    # new_menu = app.run()
    # new_menu.run()
    app.run()
    # next_console = app.run()
    # while next_console:
    #     next_console = next_console.run()



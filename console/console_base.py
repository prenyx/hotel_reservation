import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from business.UserManager import UserManager
from business.HotelManager import HotelManager
from data_access.data_base import init_db
from data_models.models import Base, Guest, Login
from pathlib import Path


class Console(object):
    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        self._database_path = database_path  # store the database_path as an instance variable

    def run(self) -> Optional['Console']:
        # Implementation für main file
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
        for i, option in enumerate(self._options, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("#" * self._width)

    def _make_choice(self) -> int:
        self._show()
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigate(self, choice: int) -> Optional[Console]:
        raise NotImplementedError("Implement this method in subclasses")

    def run(self) -> Console:
        self.clear()
        choice = self._make_choice()
        return self._navigate(choice)


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
        elif choice == 3:
            return None  # Exit


class UserRegistrationConsole(Menu):
    def __init__(self, database_path: Path):
        super().__init__("User Registration", database_path)
        self._user_manager = UserManager(database_path)
        self.add_option(MenuOption("Create New Login"))
        self.add_option(MenuOption("Register Existing User"))
        self.add_option(MenuOption("Back to Main Menu"))

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            self.create_new_login()
            return self
        elif choice == 2:
            self.register_existing_user()
            return self
        elif choice == 3:
            return StartConsole(self._database_path)

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


class HotelManagementConsole(Menu):
    def __init__(self, database_path: Path):
        super().__init__("Hotel Management", database_path)
        self._hotel_manager = HotelManager(database_path)
        self.add_option(MenuOption("Add Hotel"))
        self.add_option(MenuOption("Remove Hotel"))
        self.add_option(MenuOption("Update Hotel Info"))
        self.add_option(MenuOption("View All Bookings"))
        self.add_option(MenuOption("Edit Booking"))
        self.add_option(MenuOption("Manage Room Availability"))
        self.add_option(MenuOption("Update Room Price"))
        self.add_option(MenuOption("Back to Main Menu"))

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            name = input("Enter hotel name: ")
            stars = input("Enter hotel stars: ")
            street = input("Enter hotel street: ")
            zip_code = input("Enter hotel zip code: ")
            city = input("Enter hotel city: ")

            self._hotel_manager.add_hotel(name, stars, street, zip_code, city)
        elif choice == 2:
            hotel_id = input("Enter hotel ID to remove: ")
            self._hotel_manager.remove_hotel(hotel_id)
        elif choice == 3:
            hotel_id = int(input("Enter hotel ID to update: "))
            print("Enter the new values (leave blank to keep current value):")
            name = input("Enter new hotel name: ")
            stars = input("Enter new hotel stars: ")
            street = input("Enter new streetname: ")
            city = input("Enter new city: ")
            zip = input("Enter new zip code: ")

            updates = {}
            if name:
                updates['name'] = name
            if stars:
                updates['stars'] = int(stars)
            if street:
                updates['street'] = street
            if city:
                updates['city'] = city
            if zip:
                updates['zip_code'] = zip

            hotel = self._hotel_manager.update_hotel(hotel_id, **updates)
            if hotel:
                print(f"Hotel updated: {hotel}")
            else:
                print("Hotel not found.")
        elif choice == 4:
            self._hotel_manager.view_all_bookings()
        elif choice == 5:
            booking_id = input("Enter booking ID to update: ")
            phone_number = input("Enter new phone number (or press Enter to skip): ")
            self._hotel_manager.edit_booking(booking_id, phone_number if phone_number else None)
        elif choice == 6:
            hotel_id = input("Enter hotel ID: ")
            room_number = input("Enter room number: ")
            available = input("Is the room available? (yes/no): ").lower() == 'yes'
            self._hotel_manager.manage_room_availability(hotel_id, room_number, available)
        elif choice == 7:
            hotel_id = input("Enter hotel ID: ")
            room_number = input("Enter room number: ")
            price = input("Enter new price: ")
            self._hotel_manager.update_room_price(hotel_id, room_number, price)
        elif choice == 8:
            return StartConsole(self._database_path)
        return self


if __name__ == "__main__":
    database_path = Path("../data/my_db.db")
    app = Application(StartConsole(database_path))
    app.run()

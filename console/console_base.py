import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from business.UserManager import UserManager
from business.HotelManager import HotelManager
from data_access.data_base import init_db
from data_models.models import Base, Guest, Login, Room, Booking

from datetime import datetime
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
        self.add_option(MenuOption("Add Room"))
        self.add_option(MenuOption("Remove Hotel"))
        self.add_option(MenuOption("Remove Room"))
        self.add_option(MenuOption("Update Hotel Info"))
        self.add_option(MenuOption("View All Bookings"))
        self.add_option(MenuOption("Edit Booking"))
        self.add_option(MenuOption("Manage Room Availability"))
        self.add_option(MenuOption("Update Room Price"))
        self.add_option(MenuOption("Back to Main Menu"))

    def _navigate(self, choice: int) -> Optional[Console]:
        session = self._hotel_manager.get_session()
        if choice == 1:
            name = input("Enter hotel name: ")
            stars = input("Enter hotel stars: ")
            street = input("Enter hotel street: ")
            zip_code = input("Enter hotel zip code: ")
            city = input("Enter hotel city: ")

            self._hotel_manager.add_hotel(name, stars, street, zip_code, city)

        elif choice == 2:
            hotel_id = input("Enter for which Hotel you want to add a new Room")
            # shows the user all existing room ids as an overview, before letting the user add a new one
            rooms = session.query(Room).filter_by(hotel_id=hotel_id).all()
            for room in rooms:
                print(f"Existing Room ID: {room.number}")

            number = input("Enter room number: ")
            type = input("Enter room type (single room, double room, family room or suite): ")
            max_guests = input("Enter maximum amount of guests allowed: ")
            description = input("Enter room description: ")
            amenities = input("Enter room amenities: ")
            price = input("Enter room price: ")

            self._hotel_manager.add_room(hotel_id, number, type, max_guests, description, amenities, price)
        elif choice == 3:
            hotel_id = input("Enter hotel ID to remove: ")
            self._hotel_manager.remove_hotel(hotel_id)

        elif choice == 4:
            hotel_id = input("Enter hotel ID from which to remove a room: ")
            room_number = input("Enter room number to remove")
            self._hotel_manager.remove_room(hotel_id, room_number)

        elif choice == 5:
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
        elif choice == 6:
            self._hotel_manager.view_all_bookings()
        elif choice == 7:
            booking_id = int(input("Enter booking ID to edit: "))
            print("Enter the new values (leave blank to keep current value), be CAREFUL, "
                  "changing dates might interfere with other dates:")
            print("This function is only intended for 'brute forcing' changes on a "
                  "booking if something went wrong, otherwise it's always advised to "
                  "delete a booking and creating a new one from scratch")
            room_number = input("Enter new room number: ")
            guest_id = input("Enter new guest ID: ")
            number_of_guests = input("Enter new number of guests: ")
            start_date = input("Enter new start date (yyyy-mm-dd): ")
            end_date = input("Enter new end date (yyyy-mm-dd): ")
            comment = input("Enter new comment: ")

            updates = {}
            if room_number:
                updates['room_number'] = room_number
            if guest_id:
                updates['guest_id'] = guest_id
            if number_of_guests:
                updates['number_of_guests'] = number_of_guests
            if start_date:
                updates['start_date'] = start_date
            if end_date:
                updates['end_date'] = end_date
            if comment:
                updates['comment'] = comment
            booking = self._hotel_manager.edit_booking(booking_id, **updates)
            if booking:
                print(f"Booking updated: {booking}")
            else:
                print("Booking not found.")
        elif choice == 8:
            hotel_id = int(input("Enter hotel ID in which to Update availability of a room: "))
            room_number = int(input("Enter room which room number to change availability"))
            #new_availability_input = input("Enter new availability (True/False): ").lower()
            unavailability_start = input("Enter a date, from when the room is unavailable (yyyy-mm-dd): ")
            unavailability_end = input("Enter a date, from when the room is available again (yyyy-mm-dd): ")
            # if new_availability_input == 'true':
            #     new_availability = True
            # elif new_availability_input == 'false':
            #     new_availability = False
            # else:
            #     print("Invalid input. Please enter either 'True' or 'False'.")

            self._hotel_manager.change_room_availability(hotel_id, room_number, unavailability_start, unavailability_end)
        elif choice == 9:
            pass
        elif choice == 10:
            return StartConsole(self._database_path)
        return self


if __name__ == "__main__":

    database_path = Path("../data/my_db.db")
    app = Application(StartConsole(database_path))
    app.run()


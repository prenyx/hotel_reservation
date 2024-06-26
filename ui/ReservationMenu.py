from console.console_base import *
from business.ReservationManager import ReservationManager
from business.UserManager import UserManager
from business.HotelManager import HotelManager
import enum
from pathlib import Path
import datetime
import ui.mainMenu


class ResOption(enum.Enum):
    UPDATE_RESERVATION = 1
    DELETE_RESERVATION = 2
    VIEW_RESERVATION_DETAILS = 3
    VIEW_ALL_RESERVATIONS = 4
    BACK = 5


class UserType(enum.Enum):
    """A class representing the type of guest user."""
    GUEST = 1
    REGISTERED = 2


class ReservationMenu(Menu):
    def __init__(self, user_type: UserType, database_path: Path, navigate_back_function):
        """Initialise the ReservationMenu class."""
        super().__init__('Reservation Menu', database_path)
        self._hotel_manager = HotelManager(database_path)
        self.reservation_manager = ReservationManager(database_path)  # create a ReservationManager instance
        self._user_manager = UserManager(database_path)
        self._user_type = user_type
        self.add_common_options()
        self.navigate_back_function = self.navigate_back  # Navigate to main menu

        if self._user_type == UserType.GUEST:
            self.add_option(MenuOption('1. Create Reservation as Guest', self.create_reservation_as_guest))
        elif self._user_type == UserType.REGISTERED:
            self.add_option(MenuOption('2. Create Reservation as a Registered User', self.create_reservation_as_registered_user))

        self.add_option(MenuOption(str(ResOption.BACK) + " Back to Main Menu", self.navigate_back))

    def add_common_options(self):
        """Adds menu options that are common to all user types."""
        self.add_option(MenuOption("Update Reservation", self.update_reservation))
        self.add_option(MenuOption("Delete Reservation", self.delete_reservation))
        self.add_option(MenuOption("View Reservation Details", self.view_reservation_details))
        self.add_option(MenuOption("View all Reservations", self.list_reservations))

    def wait_for_user_input(self):
        """A helper method that waits for user input before returning."""
        input('Press Enter to continue...')

    def create_reservation_as_guest(self):
        """Create a reservation for the guest user."""
        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        email = input("Enter your email: ")
        street = input("Enter your address: ")
        zip_code = input("Enter your zip code: ")
        city = input("Enter your city: ")

        start_date = input("Please enter start date of reservation in dd-mm-YYYY format: ")
        end_date = input("Please enter end date of reservation in dd-mm-YYYY format: ")

        guest = self._user_manager.create_guest(firstname=firstname, lastname=lastname, street=street, email=email,
                                                zip_code=zip_code, city=city)

        # If guest is not None, proceed with reservation
        if guest:
            # Fetch the hotel id using hotel's name
            hotel_name = input("Enter your hotel name: ")  # get the hotel's name as user input
            hotel_id = self._hotel_manager.get_hotel_id_by_name(hotel_name)  # get hotel's id

            if not hotel_id:
                print('No such hotel found. Please try again.')
                self.wait_for_user_input()
                return

            available_rooms = self.reservation_manager.check_available_rooms(hotel_id, start_date, end_date)

            if not available_rooms:
                print('No rooms are available for the given date range.')
                self.wait_for_user_input()
                return

            room_to_book = available_rooms[0]  # Booking the first available room

            number_of_guests = input(f"Enter number of guests (Max {room_to_book.max_guests}): ")
            comment = input("Enter any specific comments (Press Enter for None): ")

            # Proceed with the reservation creation
            self.reservation_manager.create_reservation(guest.id, room_to_book.hotel_id, room_to_book.number,
                                                        number_of_guests, start_date, end_date, comment)
            print('Reservation created successfully.')
        else:
            print('Failed to create reservation. No reservation has been created!')
        self.wait_for_user_input()

    def create_reservation_as_registered_user(self):
        """Create a reservation for a registered user."""
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # Use the UserManager to authenticate the user.
        user = self._user_manager.register_existing_user(email, password)

        # Ensure user exists
        if user is None:
            print('Invalid credentials. Please try again.')

        self.wait_for_user_input()

    def update_reservation(self):
        """Update an existing reservation."""
        print("Updating a reservation...")

        try:
            reservation_id = int(input("Enter reservation ID: "))
            number_of_guests = int(input("Enter new number of guests: "))
        except ValueError:
            print('Invalid input type. Please enter a number')

        # Call the reservation manager to update the reservation
        updated_reservation = self.reservation_manager.update_reservation(reservation_id,
                                                                          number_of_guests=number_of_guests)
        # Check if update was successful
        if updated_reservation is None:
            print(f'Failed to update reservation {reservation_id}. Please check your reservation ID and try again.')
        else:
            print("Reservation successfully updated:")
        self.wait_for_user_input()

    def delete_reservation(self):
        """Delete an existing reservation."""
        print("Deleting a reservation...")

        try:
            reservation_id = int(input("Enter reservation ID: "))
        except ValueError:
            print('Invalid input type. Please enter a number')
            return

        successfully_deleted = self.reservation_manager.delete_reservation(reservation_id)

        if successfully_deleted:
            print("Reservation successfully deleted.")
        else:
            print("Failed to delete the reservation. Please check your reservation ID and try again.")
        self.wait_for_user_input()

    def view_reservation_details(self):
        """View details of a specific reservation"""
        print("Viewing reservation details...")

        try:
            reservation_id = int(input("Enter reservation ID: "))
        except ValueError:
            print('Invalid input type. Please enter a number')
            return

        # Call ReservationManager to get the reservation details
        reservation_details = self.reservation_manager.get_reservation_details(reservation_id)

        if reservation_details is None:
            print(f'No reservation found with the ID: {reservation_id}. Please check your reservation ID and try again.')
        else:
            print('Reservation details:')
            for key, value in reservation_details.items():
                print(f'{key}: {value}')
        self.wait_for_user_input()

    def list_reservations(self):
        """List all reservations."""
        print("View all reservations...")

        try:
            reservation_id = int(input("Enter the reservation ID: "))
        except ValueError:
            print('Invalid input: Please enter a number.')
            return

        reservation_details = self.reservation_manager.get_reservation_details(reservation_id)

        # Check if operation was successful
        if reservation_details is None:
            print(f"No reservation found with the ID: {reservation_id}. Please check your reservation ID and try again.")
        else:
            print("Reservation Details:")
            for key, value in reservation_details.items():
                if key in ['room', 'guest']:
                    print(f"{key.capitalize()} Details:")
                    for subkey, subvalue in value.items():
                        print(f"{subkey}: {subvalue}")
                else:
                    print(f"{key}: {value}")
        self.wait_for_user_input()

    def navigate_back(self):
        """Navigation process for back option"""
        return self.navigate_back_function

    def _navigate_common_options(self, choice: int):
        navigation_reservation_option = ResOption(choice)
        navigate_function = self.get_options()[navigation_reservation_option.value - 1].get_action()
        return navigate_function()

    def _navigate_user_type(self, choice: int):
        navigation_user_option = UserType(choice)
        navigate_function = self.get_options()[navigation_user_option.value - 1].get_action()
        return navigate_function()


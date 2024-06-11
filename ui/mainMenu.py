from console.console_base import Menu, MenuOption
from pathlib import Path
from SearchMenu import SearchMenu
from business.ReservationManager import *
from business.UserManager import *


class MainMenu(Menu):
    def __init__(self):
        """Initialise the MainMenu class."""
        super().__init__()
        self.search_menu = SearchMenu()
        self.reservation_menu = ReservationMenu()
        self.add_option(MenuOption("Search Hotels", self.search_menu))
        self.add_option(MenuOption("Reservation Menu", self.reservation_menu))
        self.add_option(MenuOption("Quit", None))

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self.search_menu
            case 2:
                return self.reservation_menu
            case 3:
                return None
            case _:
                print("Invalid choice. Please try again.")
                return self


class ReservationMenu(Menu):
    def __init__(self, user_type: str, mein_menu: Menu):
        """Initialise the ReservationMenu class."""
        super().__init__('Reservation Menu')
        self.reservation_manager = ReservationManager()  # create a ReservationManager instance
        self._user_manager = UserManager()
        self._user_type = user_type
        self.add_common_options()

        if self._user_type == 'guest':
            self.add_option(MenuOption('Create Reservation as Guest', self.create_reservation_as_guest()))
        elif self._user_type == 'registered_user':
            self.add_option(MenuOption('Create Reservation as a Registered User', self.create_reservation_as_registered_user()))

        self.add_option(MenuOption('Back to Main Menu', None))

    def add_common_options(self):
        """Adds menu options that are common to all user types."""
        self.add_option(MenuOption("Update Reservation", self.update_reservation))
        self.add_option(MenuOption("Delete Reservation", self.delete_reservation))
        self.add_option(MenuOption("View Reservation Details", self.view_reservation_details))
        self.add_option(MenuOption("View all Reservations", self.list_reservations))
        self.add_option(MenuOption("Back to Main Menu", None))

    def create_reservation_as_guest(self):
        """Create a reservation for the guest user."""
        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")
        email = input("Enter your email: ")
        street = input("Enter your street name: ")
        city = input("Enter your city: ")

        guest = self._user_manager.create_guest(firstname, lastname, email, street, city)

        # Now proceed with the reservation creation
        self.reservation_manager.create_reservation(guest.id)

    def create_reservation_as_registered_user(self):
        """Create a reservation for a registered user."""
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # Use the UserManager to authenticate the user.
        user = self._user_manager.register_existing_user(email, password)

        # Ensure user exists
        if user is None:
            print('Invalid credentials. Please try again.')
            return

    def update_reservation(self):
        """Update an existing reservation."""
        print("Updating a reservation...")

        try:
            reservation_id = int(input("Enter reservation ID: "))
            number_of_guests = int(input("Enter new number of guests: "))
        except ValueError:
            print('Invalid input type. Please enter a number')
            return

        # Call the reservation manager to update the reservation
        updated_reservation = self.reservation_manager.update_reservation(reservation_id,
                                                                          number_of_guests=number_of_guests)
        # Check if update was successful
        if updated_reservation is None:
            print(f'Failed to update reservation {reservation_id}. Please check your reservation ID and try again.')
        else:
            print("Reservation successfully updated:")

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

    def view_reservation_details(self):
        """View details of a specific reservation"""
        print("Viewing reservation details...")

        try:
            reservation_id = int(input("Enter reservation ID: "))
        except ValueError:
            print('Invalid input type. Please enter a number')
            return

        reservation_details = self.reservation_manager.get_reservation_details(reservation_id)

        if reservation_details is None:
            print(f'No reservation found with the ID: {reservation_id}. Please check your reservation ID and try again.')
        else:
            print('Reservation details:')
            for key, value in reservation_details.items():
                print(f'{key}: {value}')

    def list_reservations(self):
        """List all reservations."""
        print("View all reservations...")

        try:
            reservation_id = int(input("Enter the reservation ID: "))
        except ValueError:
            print('Invalid input: Please enter a number.')
            return

        # Call ReservationManager to get the reservation details
        reservation_details = self.reservation_manager.get_reservation_details(reservation_id)

        # Check if operation was successful
        if reservation_details is None:
            print(
                f"No reservation found with the ID: {reservation_id}. Please check your reservation ID and try again.")
        else:
            print("Reservation Details:")
            for key, value in reservation_details.items():
                if key in ['room', 'guest']:
                    print(f"{key.capitalize()} Details:")
                    for subkey, subvalue in value.items():
                        print(f"{subkey}: {subvalue}")
                else:
                    print(f"{key}: {value}")

# if __name__ == "__main__":
#     database_path = Path("hotel_reservation.db")
#     reservation_manager = ReservationManager(database_path)
#     reservation_menu = ReservationMenu(reservation_manager)
#     reservation_menu.run()


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()

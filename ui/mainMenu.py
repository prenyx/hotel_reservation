import enum
from pathlib import Path

from console.console_base import *
from .ReservationMenu import ReservationMenu, UserType
from .SearchMenu import SearchMenu
from business.SearchManager import SearchManager
from business.ReservationManager import ReservationManager


class OptionMainMenu(enum.Enum):
    SEARCH_VIEW_HOTELS = 1
    RESERVATION_MENU = 2
    LOGIN_MENU = 3
    QUIT = 4


class MainMenu(Menu):
    def __init__(self, database_path: Path):
        """Initialise the MainMenu class."""
        super().__init__('Main Menu', database_path)
        self.search_menu = SearchMenu(database_path, self.navigate_back())
        self.reservation_menu = ReservationMenu(UserType.GUEST, database_path, self.navigate_back())  # Default user
        self.user_registration_menu = UserRegistrationConsole(database_path, self.navigate_back())
        self.hotel_management_menu = HotelManagementConsole(database_path, self.navigate_back())
        self.add_option(MenuOption('1. Search and view Hotel details', self.search_menu.run))
        self.add_option(MenuOption("2. Booking Menu", self.reservation_menu.run, self.navigate_back))
        self.add_option(MenuOption('3. Login for admin', self.user_registration_menu.run))
        self.add_option(MenuOption("4. Quit", self.quit))

    def display(self):
        """Prints out the main menu options along with their description."""
        print('\nWelcome to the hotel reservation system!')

        for option in self._options:
            option_index = OptionMainMenu[option.description.upper().replace(' ', '_')].value  # Get menu index from enum
            print(f'{option_index}. {option.description}')

    def navigate_back(self):
        return self  # Here, 'self' is an instance of MainMenu

    def quit(self):
        """Close the program"""
        print('Thank you for using this program! See you next time!')
        return None  # Could use `sys.exit()`

    def _navigate(self, choice: int):
        """Process menu navigation"""
        navigation_option = OptionMainMenu(choice)  # Converted to Enum
        navigation_function = self.get_options()[navigation_option.value - 1].get_action()
        return navigation_function()

    def run(self):
        """Run the menu in a loop until user quits the program."""
        while True:
            self.display()  # Display welcome message
            user_choice = input('Please select an action: ')

            # Check to see if the input is a digit and within the range of options
            if user_choice.isdigit():
                user_choice = int(user_choice)
                if 1 <= user_choice <= len(self._options):
                    navigation_result = self._navigate(user_choice)
                    if navigation_result == 4:
                        break
                else:
                    print('Invalid choice. Please choose a number from the menu options.')
            else:
                print('Invalid input. Enter a number.')


#
# if __name__ == "__main__":
#     menu = MainMenu()
#     menu.run()

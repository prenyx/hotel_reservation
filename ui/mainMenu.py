import enum

from console.console_base import *
from pathlib import Path
from SearchMenu import SearchMenu
from ReservationMenu import *
from business.ReservationManager import *
from business.UserManager import *


class OptionMainMenu(enum.Enum):
    SEARCH_VIEW_HOTELS = 1
    RESERVATION_MENU = 2
    LOGIN_MENU = 3
    QUIT = 4


class MainMenu(Menu):
    def __init__(self):
        """Initialise the MainMenu class."""
        super().__init__()
        self.search_menu = SearchMenu()
        self.reservation_menu = ReservationMenu(UserType.GUEST)  # Default user
        self.user_registration_menu = UserRegistrationConsole()
        self.hotel_management_menu = HotelManagementConsole()
        self.add_option(MenuOption('1. Search and view Hotel details', self.search_menu.run))
        self.add_option(MenuOption("2. Booking Menu", self.reservation_menu.run))
        self.add_option(MenuOption('3. Login for admin', self.user_registration_menu.run))
        self.add_option(MenuOption("4. Quit", self.quit))

    def display(self):
        """Prints out the main menu options along with their description."""
        print('\nWelcome to the hotel reservation menu! Please select an action: ')

        for option in self._options:
            option_index = OptionMainMenu[option.description.upper().replace(' ', '_')].value  # Get menu index from enum
            print(f'{option_index}. {option.description}')

    def quit(self):
        """Close the program"""
        print('Thank you for using this program! See you next time!')
        return None  # Could use `sys.exit()`

    def _navigate(self, choice: int):
        """Process menu navigation"""
        navigation_option = OptionMainMenu(choice)  # Converted to Enum
        navigation_function = self.get_options()[navigation_option.value - 1].get_action()
        return navigation_function()

#
# if __name__ == "__main__":
#     menu = MainMenu()
#     menu.run()

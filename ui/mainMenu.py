import enum
import sys

from console.console_base import *
from .ReservationMenu import ReservationMenu, UserType
from .SearchMenu import SearchMenu


class OptionMainMenu(enum.Enum):
    SEARCH_VIEW_HOTELS = 1
    RESERVATION_MENU = 2
    LOGIN_MENU = 3
    QUIT = 4


class MainMenu(Menu):
    def __init__(self, database_path: Path):
        """Initialise the MainMenu class."""
        super().__init__('Main Menu', database_path)
        self.search_menu = SearchMenu(database_path, self.navigate_back)
        self.reservation_menu = ReservationMenu(UserType.GUEST, database_path, self.navigate_back)  # Default user
        self.user_registration_menu = UserRegistrationConsole(database_path, self.navigate_back)
        self.hotel_management_menu = HotelManagementConsole(database_path, self.navigate_back)
        self.add_option(MenuOption('Search and view Hotel details', self.search_menu.run))
        self.add_option(MenuOption("Booking Menu", self.reservation_menu.run))
        self.add_option(MenuOption('Login for admin', self.user_registration_menu.run))
        self.add_option(MenuOption("Quit", self.quit))

    def display(self):
        """Prints out the main menu options along with their description."""
        print('\nWelcome to the hotel reservation system!')

        for option in self._options:
            option_index = self._options.index(option) + 1  # Get menu index from enum. 1. Enum not needed here
            print(f'{option_index}. {option.get_title()}')

    def navigate_back(self):
        return self  # Here, 'self' is an instance of MainMenu

    def quit(self):
        """Close the program"""
        print('Thank you for using this program! See you next time!')
        sys.exit()

    def _navigate(self, choice: int):
        """Process menu navigation."""
        # Decrease the choice by 1 to align with Python's 0-indexing
        navigation_function = self.get_options()[choice - 1].get_action()
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

from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption


class SearchMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Search by city"))  # option 1
        self.add_option(MenuOption("Search by city and stars"))  # option 2
        self.add_option(MenuOption("Search by city and guest count"))  # option 3
        # TODO: Add further MenuOptions to search by the address.city etc. of the hotels.
        self.add_option(MenuOption("Back"))  # option 4
        # we need the main menu to navigate back to it
        self.__main_menu = main_menu

        self.__search_manager = SearchManager()

    @staticmethod  # Static method because we are not calling or modifying any instance variables within this method
    def wait_for_user_input():
        """A helper method that waits for user input before returning."""
        input('Press Enter to continue...')

    def __search_by_city(self):
        """Function to search hotels by city."""
        self.clear()  # clear the console
        city = input('City: ').strip()  # trim spaces

        if city:
            hotels_in_city = self.__search_manager.search_hotels_by_city(city)  # search by city with the search manager
            if not hotels_in_city:
                print('No hotels found in the city -', city)
            else:
                for hotel in hotels_in_city:
                    print(hotel)

    def _navigate(self, choice: int):
        match choice:
            case 1:  # option 1 (Show all hotel)
                self.__show_all()
                return self  # navigate again to this menu
            case 2:  # option 2 (Search by name)
                self.__search_by_city()
                return self  # navigate again to this menu
            case 3:  # option 3 (Search by starts)
                self.__search_by_stars()
                return self  # navigate again to this menu
            # TODO: Add further navigation options according to the added MenuOptions in the constructor.
            case 4:  # option 4 (Back)
                return self.__main_menu  # navigate back to the main menu

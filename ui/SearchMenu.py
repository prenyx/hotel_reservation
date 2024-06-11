from business.SearchManager import SearchManager
from console.console_base import Menu, MenuOption
import datetime

CITY_SEARCH_OPTION = 1
STAR_SEARCH_OPTION = 2
CITY_GUEST_SEARCH_OPTION = 3
DATE_GUEST_SEARCH_OPTION = 4
DISPLAY_HOTEL_DETAILS_OPTION = 5
ROOM_CITY_SEARCH_OPTION = 6
BACK_OPTION = 7


class SearchMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__("Search Hotel")
        self.add_option(MenuOption("Search by city"))  # option 1
        self.add_option(MenuOption("Search by city and stars"))  # option 2
        self.add_option(MenuOption("Search by city and guest count"))  # option 3
        self.add_option(MenuOption("Search by reservation date and guest count"))  # option 4
        self.add_option(MenuOption('Get all hotel details'))  # option 5
        self.add_option(MenuOption('Search by room type and city'))  # option 6
        self.add_option(MenuOption("Back"))  # option 7

        self.__main_menu = main_menu  # Navigate to main menu

        self.__search_manager = SearchManager()

    def get_date(self, prompt: str):
        while True:
            date_string = input(prompt)
            try:
                return datetime.datetime.strptime(date_string, '%d/%m/%Y')
            except ValueError:
                print('Invalid input. Please enter a date in the format DD/MM/YYYY')

    def get_guest_count(self, prompt: str):
        while True:
            try:
                guest_count = int(input(f'How many guests do you have?'))
                if guest_count <= 0:
                    print('Please enter a positive number')
                else:
                    return guest_count
            except ValueError:
                print('Invalid input. Please enter an integer.')

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
        else:
            print('Invalid city name.')
            self.wait_for_user_input()

    def __search_by_city_and_stars(self):
        """Function to search hotels by city and stars."""
        self.clear()  # clear the console
        city = input('City: ').strip()
        stars = input('Stars: ').strip()
        hotels_in_city = self.__search_manager.search_hotels_by_stars(city, stars)  # search by city and stars with search manager

        if not hotels_in_city:
            print(f'No hotels found in {city} with {stars} stars.')
        else:
            for hotel in hotels_in_city:
                print(hotel, end=' ')
        self.wait_for_user_input()

    def __search_by_guest_count(self):
        """Function to search hotels by guest count."""
        self.clear()
        city = input('City: ').strip()
        guest_count = self.get_guest_count()
        hotels_in_city = self.__search_manager.search_hotels_by_guest_count(city, guest_count)

        if not hotels_in_city:
            print(f'No hotels found in {city} with {guest_count} guests.')
        else:
            for hotel in hotels_in_city:
                print(hotel, end=' ')
        self.wait_for_user_input()

    def __search_by_date_guest_count(self):
        """Function to search hotels by reservation date and guest count."""
        start_date = self.get_date('Enter the start date for your reservation (DD/MM/YYYY): ')
        get_guest_count = self.get_guest_count('Enter the number of guests you will bring with: ')
        end_date = self.get_date('Enter the end date for your reservation (DD/MM/YYYY): ')

        hotels = self.__search_manager.search_hotels_by_date_and_guest_count(start_date, end_date, get_guest_count)

        if not hotels:
            print('No hotels available for the given criteria.')
            self.wait_for_user_input()
        else:
            for hotel in hotels:
                print(hotel)
        self.wait_for_user_input()

    def __get_all_hotel_details(self):
        """Function to get all hotel details and its availability."""

        # Fetch all the hotel details
        hotel_details = self.__search_manager.get_all_hotel_details()

        if not hotel_details:
            print('No hotels found')
            self.wait_for_user_input()

        print('Hotel details:')
        for hotel in hotel_details:
            print('--------------------')
            print(f'Hotel Name: {hotel.name}')
            print(f'Hotel Address: {hotel.address}')
            print(f'Hotel Rating: {hotel.stars} stars')
            print('Room Details:')
            for room in hotel.rooms:
                print(f'Room Number: {room.number}, Room Type: {room.type}, Maximum Guests: {room.max_guests}')
                print(f'Room Description: {room.description}')
                print(f'Room Type: {room.type}')
                print(f'Room Price: {room.price}')

                # Display room's availability status.
                if room.unavailability_start is not None and room.unavailability_end is not None:
                    print(f'Room Availability: Unavailable from {room.unavailability_start} to {room.unavailability_end}')
                else:
                    print('Room Availability: Available')
        print('--------------------')

    def __search_by_room_type_city(self):
        """Function to search hotels by room type and city."""

        room_type = input('Please enter your desired room type (Single, Double, Suite).: ')
        city = input('In which city would you like to stay?: ')

        # Fetch the rooms with given room type and city.
        rooms = self.__search_manager.get_rooms_by_type_and_city(room_type, city)

        if not rooms:
            print('No rooms found')
            self.wait_for_user_input()

        print('Room Details:')
        for room in rooms:
            print(f'Hotel Name: {room.name}, Room Nr. {room.number}\nRoom Type: {room.type}')
            print(f'Max Guests: {room.max_guests}\nDescription: {room.description}\nprice: {room.price}')
            print(f'Availability: {'Unavailable' if room.unavailability_start and room.unavailability_end else 'Available'}')
            print('--------------------')

    def navigate_city_search(self):
        """Navigation process for city search"""
        self.__search_by_city()
        return self

    def navigate_star_search(self):
        """Navigation process for star search"""
        self.__search_by_city_and_stars()
        return self

    def navigate_guest_search(self):
        """Navigation process for guest count search"""
        self.__search_by_guest_count()
        return self

    def navigate_date_guest_search(self):
        """Navigation process for reservation date and guest count search"""
        self.__search_by_date_guest_count()
        return self

    def navigate_get_all_hotel_details(self):
        """Navigation process for get all hotel details"""
        self.__get_all_hotel_details()
        return self

    def navigate_room_city_search(self):
        """Navigation process for room_type and city search"""
        self.__search_by_room_type_city()
        return self

    def navigate_back(self):
        """Navigation process for back option"""
        return self.__main_menu

    def _navigate(self, choice: int):
        if choice == CITY_SEARCH_OPTION:
            return self.navigate_city_search()
        elif choice == STAR_SEARCH_OPTION:
            return self.navigate_star_search()
        elif choice == CITY_GUEST_SEARCH_OPTION:
            return self.navigate_guest_search()
        elif choice == DATE_GUEST_SEARCH_OPTION:
            return self.navigate_date_guest_search()
        elif choice == DISPLAY_HOTEL_DETAILS_OPTION:
            return self.navigate_get_all_hotel_details()
        elif choice == ROOM_CITY_SEARCH_OPTION:
            return self.navigate_room_city_search()
        elif choice == BACK_OPTION:
            return self.navigate_back()

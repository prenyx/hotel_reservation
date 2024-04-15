class HotelCollection:
    """A collection of hotels"""

    def __init__(self):
        self.hotels = dict()

    def add_hotel(self, name, location, hotel):
        # Here use hotel name and location as unique identifier for each hotel object
        self.hotels[f"{name}@{location}"] = hotel


# Create a global Hotel Collection instance.
hotel_collection = HotelCollection()


class Hotel:
    """A hotel class represents a single hotel"""

    def __new__(cls, *args, **kwargs):
        # Create the object (calls object.__new__ method)
        new_obj = super().__new__(cls)
        # Add this object to the hotel collection
        hotel_collection.add_hotel(args[0], args[1], new_obj)
        return new_obj

    def __init__(self, name, location, rating, rooms):
        self.__name = name
        self._location = location
        self._rating = rating
        self.__rooms = rooms

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self._location

    @property
    def rating(self):
        return self._rating

    @property
    def rooms(self):
        return self.__rooms


if __name__ == "__main__":
    hotel1 = Hotel('Aria', 'London', 4, 450)
    hotel2 = Hotel('Aria', 'Paris', 5, 550)
    print(hotel_collection.hotels)

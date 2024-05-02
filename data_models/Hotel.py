import dataclasses
from typing import List
from Room import Room


@dataclasses.dataclass
class Address:
    id: int
    street: str
    zip_code: int
    city: str
    country: str


@dataclasses.dataclass
class Hotel:
    """A class representing a hotel."""
    hotel_id: int
    name: str
    address: Address
    rating: float
    rooms: List['Room'] = dataclasses.field(default_factory=list)

    def add_room(self, room: 'Room'):
        """Add a room to the hotel"""
        self.rooms.append(room)


if __name__ == '__main__':
    address1 = Address(1, 'rue example 1', 54632, 'Paris', 'France')
    address2 = Address(2, 'example street', 5316, 'New York', 'USA')
    hotel1 = Hotel(1, 'Aria', address1, 5)
    hotel2 = Hotel(2, 'Aria', address2, 4)
    hotels = [hotel1, hotel2]
    print(hotels)

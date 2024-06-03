# Simple structure for Hotel Manager
# e.g. Admin fuctionalities (manipulate hotels, users, show all bookings etc.)

#3. Als Admin-Nutzer:
#3.1. Als Admin-Nutzer des Buchungssystems möchte ich die Möglichkeit
#haben, Hotelinformationen zu pflegen, um aktuelle Informationen im System
#zu haben.
#3.1.1. Ich möchte neue Hotels zum System hinzufügen
#3.1.2. Ich möchte Hotels aus dem System entfernen
#3.1.3. Ich möchte die Informationen bestimmter Hotels aktualisieren, z. B. den Namen, die Sterne usw.
#3.2. Als Admin-Nutzer des Buchungssystems möchte ich alle Buchungen aller Hotels sehen können, um eine Übersicht zu erhalten.
#3.3. Ich möchte alle Buchungen bearbeiten können, um fehlende Informationen zu ergänzen (z.B. Telefonnummer) [Optional].
#(3.4. Ich möchte in der Lage sein, die Zimmerverfügbarkeit zu verwalten und
#die Preise in Echtzeit im Backend-System der Anwendung zu aktualisieren [Optional].)

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session, sessionmaker
from data_models.modelsOld import *

from data_access.data_base import init_db
class HotelManager(object):
    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get_session(self):
        return self.__session

    # 3.1.1. Add new hotels to the system
    def add_hotel(self):
        session = self.get_session()

        name = input("Hotel Name: ")
        stars = input("Hotel Stars: ")
        street = input("Enter street: ")
        zip_code = input("Enter zip code: ")
        city = input("Enter city: ")

        print(f"Debug:" + street, zip_code, city)
        address = Address(street=street, zip=zip_code, city=city)
        session.add(address)
        session.commit()

        new_hotel = Hotel(name=name, stars=stars, address_=address.id)
        session.add(hotel)
        session.commit()
        return new_hotel


    # 3.1.2. Remove hotels from the system
    def remove_hotel(self, hotel_id: int):
        try:
            hotel = self.session.query(Hotel).filter(Hotel.id == hotel_id).one()
            self.session.delete(hotel)
            self.session.commit()
            return True
        except NoResultFound:
            return False

    # 3.1.3. Update hotel information
    def update_hotel(self, hotel_id: int, **kwargs):
        try:
            hotel = self.session.query(Hotel).filter(Hotel.id == hotel_id).one()
            for key, value in kwargs.items():
                if hasattr(hotel, key):
                    setattr(hotel, key, value)
            self.session.commit()
            return hotel
        except NoResultFound:
            return None

    # 3.2. View all bookings of all hotels
    def view_all_bookings(self):
        return self.session.query(Booking).all()

    # 3.3. Edit bookings to add missing information [Optional]
    def edit_booking(self, booking_id: int, **kwargs):
        try:
            booking = self.session.query(Booking).filter(Booking.id == booking_id).one()
            for key, value in kwargs.items():
                if hasattr(booking, key):
                    setattr(booking, key, value)
            self.session.commit()
            return booking
        except NoResultFound:
            return None

    # 3.4. Manage room availability and update prices in real-time [Optional]
    def update_room_availability(self, room_id: int, availability: bool):
        try:
            room = self.session.query(Room).filter(Room.id == room_id).one()
            room.available = availability
            self.session.commit()
            return room
        except NoResultFound:
            return None

    def update_room_price(self, room_id: int, new_price: float):
        try:
            room = self.session.query(Room).filter(Room.id == room_id).one()
            room.price = new_price
            self.session.commit()
            return room
        except NoResultFound:
            return None

if __name__ == "__main__":
    # Set up in-memory SQLite database for testing
    database_path = Path("../data/my_db.db")
    manager = HotelManager(database_path)

    # 3.1.1. Test add new hotel
    hotel = manager.add_hotel("Test Hotel", 5, "123 Test St", "1234567890")
    assert hotel.id is not None, "Hotel should be added with an ID"
    print("Test 3.1.1 passed: Add new hotel")

    # 3.1.2. Test remove hotel
    result = manager.remove_hotel(hotel.id)
    assert result is True, "Hotel should be removed"
    result = manager.remove_hotel(hotel.id)
    assert result is False, "Removing non-existent hotel should return False"
    print("Test 3.1.2 passed: Remove hotel")

    # Add a hotel again for further tests
    hotel = manager.add_hotel("Test Hotel", 5, "123 Test St", "1234567890")

    # 3.1.3. Test update hotel information
    updated_hotel = manager.update_hotel(hotel.id, name="Updated Test Hotel", stars=4)
    assert updated_hotel.name == "Updated Test Hotel", "Hotel name should be updated"
    assert updated_hotel.stars == 4, "Hotel stars should be updated"
    print("Test 3.1.3 passed: Update hotel information")

    # 3.2. Test view all bookings
    booking1 = Booking(hotel_id=hotel.id, guest_name="John Doe", room_number=101, check_in="2024-05-20", check_out="2024-05-25")
    booking2 = Booking(hotel_id=hotel.id, guest_name="Jane Doe", room_number=102, check_in="2024-06-01", check_out="2024-06-05")
    session.add_all([booking1, booking2])
    session.commit()
    bookings = manager.view_all_bookings()
    assert len(bookings) == 2, "There should be 2 bookings"
    print("Test 3.2 passed: View all bookings")

    # 3.3. Test edit booking [Optional]
    edited_booking = manager.edit_booking(booking1.id, guest_name="John Smith")
    assert edited_booking.guest_name == "John Smith", "Booking guest name should be updated"
    print("Test 3.3 passed: Edit booking")

    # Add a room for further tests
    room = Room(hotel_id=hotel.id, room_number=101, available=True, price=100.0)
    session.add(room)
    session.commit()

    # 3.4. Test update room availability [Optional]
    updated_room = manager.update_room_availability(room.id, False)
    assert updated_room.available is False, "Room availability should be updated"
    print("Test 3.4 passed: Update room availability")

    # 3.4. Test update room price [Optional]
    updated_room = manager.update_room_price(room.id, 150.0)
    assert updated_room.price == 150.0, "Room price should be updated"
    print("Test 3.4 passed: Update room price")

    print("All tests passed!")
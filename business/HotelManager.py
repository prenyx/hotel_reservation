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
from data_models.models import *

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
    def add_hotel(self, name, stars, street, zip_code, city):
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

        new_hotel = Hotel(name=name, stars=stars, address_id=address.id)
        session.add(new_hotel)
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

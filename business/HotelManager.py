from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from data_models.models import *
from datetime import datetime

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
        """Adds a new hotel to the database, also adds the corresponding address to the address table"""

        address = Address(street=street, zip=zip_code, city=city)
        session.add(address)
        session.commit()

        new_hotel = Hotel(name=name, stars=stars, address_id=address.id)
        session.add(new_hotel)
        session.commit()
        return new_hotel

    def add_room(self, hotel_id, number, type, max_guests, description, amenities, price):
        session = self.get_session()
        """Adds a new room to the database"""
        room = Room(hotel_id=hotel_id, number=number, type=type, max_guests=max_guests, description=description,
                    amenities=amenities, price=price)
        session.add(room)
        session.commit()

    # 3.1.2. Remove hotels from the system
    def remove_hotel(self, hotel_id: int):
        """removes a specified hotel based on the hotel id"""
        session = self.get_session()

        try:
            hotel = session.query(Hotel).filter(Hotel.id == hotel_id).one()
            session.delete(hotel)
            session.commit()
            return True
        except NoResultFound:
            return False

    def remove_room(self, hotel_id: int, room_number: int):
        """removes a specified room based on the room id"""
        session = self.get_session()

        try:
            room = session.query(Room).filter(Room.hotel_id == hotel_id).where(Room.number == room_number).one()
            session.delete(room)
            session.commit()
            return True
        except NoResultFound:
            return False

    # 3.1.3. Update hotel information
    def update_hotel(self, hotel_id: int, street=None, zip_code=None, city=None, **kwargs):
        session = self.get_session()
        """updates info of a hotel selectively only by what is provided by the user in the console"""
        try:
            hotel = session.query(Hotel).filter(Hotel.id == hotel_id).one()
            # Update hotel basic information
            for key, value in kwargs.items():
                if hasattr(hotel, key):
                    setattr(hotel, key, value)
            # Update hotel address if provided
            if street or zip_code or city:
                address = session.query(Address).filter(Address.id == hotel.address_id).one()
                if street:
                    address.street = street
                if zip_code:
                    address.zip = zip_code
                if city:
                    address.city = city
            session.commit()
            return hotel
        except NoResultFound:
            return None

    # 3.2. View all bookings of all hotels
    def view_all_bookings(self):
        """Lists all bookings of all hotels"""
        session = self.get_session()
        bookings = session.query(Booking).all()
        for booking in bookings:
            print(f"Booking ID: {booking.id}")
            print(f"Room Hotel ID: {booking.room_hotel_id}")
            print(f"Room Number: {booking.room_number}")
            print(f"Guest ID: {booking.guest_id}")
            print(f"Number of Guests: {booking.number_of_guests}")
            print(f"Start Date: {booking.start_date}")
            print(f"End Date: {booking.end_date}")
            print(f"Comment: {booking.comment}")
            print("-" * 40)

    # 3.3. Edit bookings to add missing information [Optional]
    def edit_booking(self, booking_id: int, room_number=None, guest_id=None, number_of_guest=None, start_date=None,
                     end_date=None, comment=None, **kwargs):
        """Edits booking, based on provided Info from the user in the console"""
        session = self.get_session()
        try:
            booking = session.query(Booking).filter(Booking.id == booking_id).one()
            # Update booking basic information
            for key, value in kwargs.items():
                if hasattr(booking, key):
                    setattr(booking, key, value)
            session.commit()
            return booking
        except NoResultFound:
            return None

    # 3.4. part 1: Manage room availability and update prices in real-time [Optional]
    def change_room_availability(self, hotel_id: int, room_number: str,
                                 unavailability_start: str, unavailability_end: str):
        """
        Change the availability of a room. By setting a timeframe (start and end-date) in which a room is not available.
        It then checks whether rooms are arleady booked in that timeframe (outputs it to the user) and deletes them if the user confirms.

        unavailability_start: The start date of the unavailability.
        unavailability_end: The end date of the unavailability.

        """
        # Convert the input strings to date objects
        try:
            unavailability_start = datetime.strptime(unavailability_start, '%Y-%m-%d').date()
            unavailability_end = datetime.strptime(unavailability_end, '%Y-%m-%d').date()
        except ValueError as e:
            return f"Invalid date format: {str(e)}"

        # Query for the room in question
        session = self.get_session()
        room = session.execute(select(Room).filter_by(hotel_id=hotel_id, number=room_number)).scalar_one_or_none()
        if not room:
            return f"Room {room_number} in hotel {hotel_id} does not exist."

        # Check for active bookings for this room and prints the out
        active_bookings = session.execute(
            select(Booking).filter(
                Booking.room_hotel_id == hotel_id,
                Booking.room_number == room_number,
                Booking.start_date <= unavailability_end,
                Booking.end_date >= unavailability_start
            )
        ).scalars().all()
        # iterates through all bookings if existing and prints them out
        # if confirmed, deleted all active_bookings
        if active_bookings:
            print(f"The following bookings are affected by changing availability of room {room_number}:")
            for booking in active_bookings:
                print(
                    f"Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Start Date: {booking.start_date}, End Date: {booking.end_date}")
            confirmation = input(
                "Do you want to proceed with deleting the bookings and changing the availability? (yes/no): ")
            if confirmation.lower() == 'yes':
                for booking in active_bookings:
                    session.delete(booking)
                session.commit()

            if confirmation.lower() != 'yes':
                return "Operation cancelled by user."
        else:
            print("No bookings")
        # changes the "un"-availability to user input

        room.unavailability_start = unavailability_start
        room.unavailability_end = unavailability_end
        session.commit()
        print(f"Room {room_number} availability changed to UA start{unavailability_start} and UA end{unavailability_end}.")

    # 3.4. part 2: Manage room availability and update prices in real-time [Optional] -> need to finish this part once benz finishes changes to console structure
    def update_room_price(self, room_id: int, new_price: float):
        """updates the room price"""
        try:
            room = self.session.query(Room).filter(Room.id == room_id).one()
            room.price = new_price
            self.session.commit()
            return room
        except NoResultFound:
            return None

    # Example usage:
    database_url = 'sqlite:///your_database_path_here.db'

    def get_hotel_id_by_name(self, hotel_name):
        """Fetch a hotel's id using its name."""
        session = self.get_session()
        try:
            # Query to search the hotel by its name
            hotel = session.query(Hotel).filter(Hotel.name == hotel_name).first()
            if hotel:
                return hotel.id
            else:
                print('No hotel found by this name.')
                return None
        except Exception as e:
            print(f'Error getting hotel id: {e}')
            return None
        finally:
            session.close()

# if __name__ == "__main__":
#     database_path = Path("../data/my_db.db")
#     manager = HotelManager(database_path)


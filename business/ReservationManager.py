from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from data_access.data_base import init_db

from data_models.models import *
import os
from pathlib import Path


class ReservationManager:
    """A class represents booking information"""

    # def __init__(self) -> None:
    #     self.__load_db()
    #
    # def __load_db(self):
    #     if not os.environ.get("DB_FILE"):
    #         raise ValueError("You have to define the environment variable 'DB_FILE'")
    #     self.__db_filepath = Path(os.environ.get("DB_FILE"))
    #
    #     if not self.__db_filepath.is_file():
    #         init_db(str(self.__db_filepath), generate_example_data=True)
    #
    #     self._engine = create_engine(f'sqlite:///{self.__db_filepath}')
    #     self._session = scoped_session(sessionmaker(bind=self._engine))

    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def check_room_availability(self, room_id, start_date, end_date):
        query = select(Booking).where(
            and_(
                Booking.room_id == room_id,
                or_(
                    and_(Booking.start_date <= end_date, Booking.end_date >= start_date)
                )
            )
        )
        result = self.__session.execute(query).fetchall()
        return len(result) == 0

    def check_available_rooms(session, start_date: date, end_date: date) -> List[Room]:
        """
        This function queries the database to find all rooms that are available
        between the provided start_date and end_date.

        Returns:
            A list of Room objects that are available for the given date range.
        """
        # Join Booking and Room tables to find all booked rooms during the period
        booked_rooms = (
            session.query(Room)
            .join(Booking, Booking.room_hotel_id == Room.hotel_id, Booking.room_number == Room.number)
            .filter(Booking.start_date <= end_date, Booking.end_date >= start_date)
            .all()
        )

        # Get all rooms from the Hotel table
        all_rooms = session.query(Room).all()

        # Filter out booked rooms from all rooms to find available ones
        available_rooms = [room for room in all_rooms if room not in booked_rooms]
        return available_rooms
    def book_room_as_registered_guest(self, room_id, user_id, start_date,
                                      end_date):  # do we need this, as in the user stories its only defined that guest users want to be able to book a hotel?
        if self.check_room_availability(room_id, start_date, end_date):
            new_booking = Booking(room_id=room_id, user_id=user_id, start_date=start_date, end_date=end_date)
            self.__session.add(new_booking)
            self.__session.commit()
            return new_booking

    def book_room_as_guest(self, room_id, start_date, end_date, guest_email=None):
        # This method books a room without requiring a user account
        booking = Booking(room_id=room_id, start_date=start_date, end_date=end_date, guest_email=guest_email)
        self.__session.add(booking)
        self.__session.commit()
        return booking

    def book_room(self, room_id, start_date, end_date, user_id=None, guest_email=None):
        if self.check_room_availability(room_id, start_date, end_date):
            new_booking = Booking(room_id=room_id, start_date=start_date, end_date=end_date, user_id=user_id,
                                  guest_email=guest_email)
            self.__session.add(new_booking)
            self.__session.commit()
            return new_booking
        else:
            print("Room not available for the selected dates")

    def search_hotels(self, city="", stars=None, number_of_guests=None, start_date=None, end_date=None):
        """A Method to dynamically query the database to find hotels only based on provided/partial information"""
        query = select(Hotel).join(Address, isouter=True)
        if city:
            query = query.where(Address.city.like(f"%{city}%"))
        if stars is not None:
            query = query.where(Hotel.stars == stars)
        if number_of_guests is not None:
            query = query.join(Room)
            if start_date and end_date:
                # Check room availability
                subquery = select(Booking.room_hotel_id).where(
                    and_(
                        Booking.start_date < end_date,
                        Booking.end_date > start_date
                    )
                )
                query = query.where(and_(Room.max_guests >= number_of_guests, ~Room.id.in_(subquery)))
            else:
                query = query.where(Room.max_guests >= number_of_guests)
        query = query.distinct()
        print(query)
        return self.__session.execute(query).scalars().all()

    def get_room_details(self, hotel_id):
        query = select(Room).where(Room.hotel_id == hotel_id)
        print(query)
        return self.__session.execute(query).scalars().all()

    def check_bookings_for_user(session: Session, guest_id: int, is_registered: bool = False):
        if is_registered:
            # Fetch bookings for a registered guest
            bookings = session.query(Booking).join(RegisteredGuest, Booking.guest_id == RegisteredGuest.id).filter(
                RegisteredGuest.login_id == guest_id).all()
        else:
            # Fetch bookings for a non-registered guest
            bookings = session.query(Booking).filter(Booking.guest_id == guest_id).all()
        return bookings

    def add_hotel(self, name, stars, city):
        new_hotel = Hotel(name=name, stars=stars)
        new_address = Address(city=city, hotel=new_hotel)
        self.__session.add_all([new_hotel, new_address])
        self.__session.commit()
        return new_hotel

    def update_hotel(self, hotel_id, name=None, stars=None):
        hotel = self.__session.get(Hotel, hotel_id)
        if name:
            hotel.name = name
        if stars is not None:
            hotel.stars = stars
        self.__session.commit()
        return hotel

    def delete_hotel(self, hotel_id):
        hotel = self.__session.get(Hotel, hotel_id)
        self.__session.delete(hotel)
        self.__session.commit()

    def close_session(self):
        self.__session.remove()

    # Registered User Functionalities
    # def view_booking_history_guest(self, guest_id):
    #     query = select(Booking).where(Booking.guest_id == guest_id)
    #     print(query)
    #     return self._session.execute(query).scalars().all()
    #
    #
    # def view_booking_history_guest(self, registered_guest_id):
    #     query = select(Booking).where(Booking.guest.has(id=registered_guest_id)
    #     print(query)
    #     return self._session.execute(query).scalars().all()
    #
    # def view_booking_history_registered_guest(self, guest_id):
    #     query = select(Booking).where(Booking.registered == guest_id)
    #     print(query)
    #     return self._session.execute(query).scalars().all()


def show(bookings):
    for booking in bookings:
        print(booking)


if __name__ == "__main__":
    filepath = Path("../data/our_db.db")

    rm = ReservationManager(filepath)
    rm.check_reg_user("sabrina.schmidt@bluemail.ch", "SuperSecret")

    # search_manager = SearchManager()
    room_in = input('Enter the room id: ')
    start_date_in = input('Enter the start date')
    end_date_in = input('Enter the end date')
    checked_available_rooms = rm.check_room_availability(room_in, start_date_in, end_date_in)
    show(checked_available_rooms)
    input("Press Enter to continue...")

    available_rooms = check_available_rooms(session, start_date, end_date)

    # Print available room information
    if available_rooms:
        print(f"Available rooms between {start_date} and {end_date}:")
        for room in available_rooms:
            print(f"- {room.number} ({room.type})")
    else:
        print(f"No rooms available between {start_date} and {end_date}.")

    city_in = input('City: ')
    hotels_by_city = search_manager.get_hotels_by_city(city_in)
    show(hotels_by_city)
    input("Press Enter to continue...")

    name_in = input('Name: ')
    city_in = input('City: ')
    found_hotels = search_manager.get_hotels(name_in, city_in)
    show(found_hotels)
    input("Press Enter to continue...")

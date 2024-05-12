import os
from pathlib import Path

from data_access.data_base import init_db
from sqlalchemy import select, func, create_engine, and_, not_, exists, or_
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from data_models.models import *


class SearchManager(object):
    def __init__(self) -> None:
        self.__load_db()

    def __load_db(self):
        # Ensure the environment Variable is set
        if not os.environ.get("DB_FILE"):
            raise ValueError("You have to define the environment variable 'DB_FILE'")
        self.__db_filepath = Path(os.environ.get("DB_FILE"))

        # Ensure the db file exists, if not initialize a new db with or without example data
        # You have to delete the db file, if you need a new fresh db.
        if not self.__db_filepath.is_file():
            init_db(str(self.__db_filepath), generate_example_data=True)

        self._engine = create_engine(f'sqlite:///{self.__db_filepath}')
        self._session = scoped_session(sessionmaker(bind=self._engine))

    def get_hotels(self, name: str = "", city: str = ""):
        query = select(Hotel)
        if name != "":
            query = query.where(Hotel.name.like(f'%{name}%'))
        if city != "":
            query = query.join(Address).where(Address.city.like(f"%{city}%"))

        print(query)
        return self._session.execute(query).scalars().all()

    def get_hotels_by_name(self, name: str = ""):
        query = select(Hotel)
        if name != "":
            query = query.where(Hotel.name.like(f'%{name}'))
        print(query)
        return self._session.execute(query).scalars().all()

    def get_hotels_by_city(self, city: str = ""):
        query = select(Hotel)
        if city != "":
            query = query.join(Address).where(Address.city.like(f"%{city}%"))
        print(query)
        return self._session.execute(query).scalars().all()

    def get_rooms_by_hotel(self, hotel_id: int):
        query = select(Room).where(Room.hotel_id == hotel_id)
        print(query)
        return self._session.execute(query).scalars().all()

    def get_hotels_by_criteria(self, city: str = "", stars: int = None, guest_count: int = None):
        """Method to get hotels by provided/partial criteria/s"""
        query = select(Hotel)
        if city:
            query = query.join(Address).where(Address.city.like(f"%{city}%"))
        if stars is not None:
            query = query.where(Hotel.stars >= stars)
        if guest_count is not None:
            query = query.join(Room).where(Room.max_guests >= guest_count).distinct()
        print(query)
        return self._session.execute(query).scalars().all()

    # def get_available_rooms(self, hotel_id: int, start_date, end_date, guest_count: int):
    #     query = select(Room).where(
    #         and_(
    #             Room.hotel_id == hotel_id,
    #             Room.max_guests >= guest_count,
    #             not_(exists(
    #                 select(Booking).where(
    #                     and_(
    #                         Booking.room_id == Room.id,
    #                         or_(and_(Booking.start_date <= start_date, Booking.end_date >= start_date),
    #                             and_(Booking.start_date <= end_date, Booking.end_date >= end_date))
    #                     )
    #                 )
    #             ))
    #         )
    #     )
    #     print(query)
    #     return self._session.execute(query).scalars().all()

    def check_room_availability(self, start_date, end_date, number_of_guests):
        """return available rooms that can accommodate a given number of guests and are not booked within the
        specified date range."""
        # with Session() as session:  # shall we even use this functionality?
            # Subquery to find rooms that are booked in the given date range
        subquery = select(Booking.room_number).where(
            and_(
                Booking.start_date < end_date,
                Booking.end_date > start_date
            )
        ).distinct()

        # Main query to find available rooms
        chk_available_rooms = select(Room).where(
            and_(
                Room.max_guests >= number_of_guests,
                not_(Room.number.in_(subquery))
            )
        )

        result = self._session.execute(chk_available_rooms).scalars().all()
        if result:
            return result
        else:
            return "No rooms found in that timeframe."


def show(hotels):
    for hotel in hotels:
        print(hotel)


if __name__ == '__main__':
    # This is only for testing without Application

    # You should set the environment variable in the run configuration.
    # However, we can set it here in python as well.
    # Because we are executing this file in the folder ./business/
    # we need to relatively navigate first one folder up and therefore,
    # use ../data in the path instead of ./data
    # if the environment variable is not set, set it to a default
    if not os.environ.get("DB_FILE"):
        os.environ["DB_FILE"] = input("Enter relative Path to db file: ")
        while not Path(os.environ.get("DB_FILE")).parent.is_dir():
            os.environ["DB_FILE"] = input("Enter relative Path to db file: ")
    search_manager = SearchManager()
    all_hotels = search_manager.get_hotels()
    show(all_hotels)
    all_hotels = search_manager.get_hotels()
    input("Press Enter to continue...")

    city_in = input('City: ')
    hotels_by_city = search_manager.get_hotels_by_city(city_in)
    show(hotels_by_city)
    input("Press Enter to continue...")

    name_in = input('Name: ')
    city_in = input('City: ')
    found_hotels = search_manager.get_hotels(name_in, city_in)
    show(found_hotels)
    input("Press Enter to continue...")

    # Example dates and guest number
    start = date(2024, 5, 20)
    end = date(2024, 5, 25)
    guests = 2

    available_rooms = search_manager.check_room_availability(start, end, guests)
    for room in available_rooms:
        print(room)

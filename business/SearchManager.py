import os
from pathlib import Path

from data_access.data_base import init_db
from sqlalchemy import select, func, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import \
    and_  # commonly used in query filters to allow multiple filter conditions, equivalent to the logical operator AND in SQL

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

    def get_hotels(self, filters):
        query = select(Hotel)
        for attr, value in filters.items():
            if value:
                query = self.add_filter(query, attr, value)

        room_type = filters.get('room_type')
        if room_type:
            query = query.join(Hotel.rooms).filter(Room.type.like(f'%{room_type}%'))
        return self._session.execute(query).scalars().all()

    def add_filter(self, query, attr, value):
        """docstring for add_filter"""
        field = getattr(Hotel, attr, None)
        if field:
            if attr == 'price':
                return query.where(and_(field >= value['min'], field <= value['max']))
            elif attr == 'rating':
                return query.where(field == float(value))
            elif attr == 'availability':
                return query.where(field == value)
            elif attr in ['name', 'city', 'amenities']:
                return query.where(field.like(f'%{value}%'))
        return query


def show(hotels):
    for hotel in hotels:
        print(f"Hotel Name: {hotel.name}, City: {hotel.city}, Rating: {hotel.rating}")


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

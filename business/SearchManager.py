import os
from pathlib import Path

from data_access.data_base import init_db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, and_, or_
from data_models.models import *


class SearchManager:
    def __init__(self, database_path: Path):
        """Initialize the SearchManager class"""
        if not database_path.is_file():  # Checks if a DB file already exists
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get_session(self):
        return self.__session()

    def search_hotels_by_city(self, city_name):
        """Get all hotels searched by city name"""
        session = self.get_session()
        try:
            results = session.query(Hotel).join(Address).filter(Address.city == city_name).all()
            return results
        except Exception as e:
            print(f'Error searching hotels by city: {e}')
            return None
        finally:
            session.close()

    def search_hotels_by_stars(self, city_name, stars):
        session = self.get_session()
        try:
            results = session.query(Hotel).join(Address).filter(
                and_(Address.city == city_name, Hotel.stars == stars)).all()
            return results
        except Exception as e:
            print(f'Error searching hotels by stars: {e}')
            return None
        finally:
            session.close()

    def search_hotels_by_guest_count(self, city_name, guest_count=int):
        session = self.get_session()
        try:
            results = session.query(Hotel).join(Address).join(Room).filter(
                and_(Address.city == city_name, Room.max_guests >= guest_count)).all()
            return results
        except Exception as e:
            print(f'Error searching hotels by guest count: {e}')
            return None
        finally:
            session.close()

    def search_hotels_by_date_and_guest_count(self, city_name, guest_count, start_date, end_date):
        session = self.get_session()
        try:
            subquery = session.query(Room.hotel_id).join(Booking).filter(
                and_(
                    Booking.start_date <= end_date,
                    Booking.end_date >= start_date,
                    Booking.number_of_guests >= guest_count
                )
            ).subquery()
            results = session.query(Hotel).join(Address).join(Room).filter(
                and_(
                    Address.city == city_name,
                    Room.hotel_id.notin_(subquery)
                )
            ).all()
            return results
        except Exception as e:
            print(f'Error searching hotels by date and guest count {e}')
            return None
        finally:
            session.close()

    def get_hotel_details(self, hotel_id, city):
        session = self.get_session()
        try:
            hotel = session.query(Hotel).filter(Hotel.id == hotel_id).first()
            city = session.query(Address).filter(Address.city == city).all()
            if hotel:
                return {
                    'name': hotel.name,
                    'address': hotel.address,
                    'city': city,
                    'stars': hotel.stars
                }
            return None
        except Exception as e:
            print(f'Error getting hotel details: {e}')
            return None
        finally:
            session.close()

    def get_all_hotel_details(self):
        session = self.get_session()
        try:
            hotels = session.query(Hotel).all()
            return [{'name': hotel.name, 'address': hotel.address, 'stars': hotel.stars} for hotel in hotels]
        except Exception as e:
            print(f'Error getting hotel details: {e}')
            return []
        finally:
            session.close()

    def get_room_details(self, hotel_id, room_type=None):
        session = self.get_session()
        try:
            query = session.query(Room).filter(Room.hotel_id == hotel_id)

            # Add room_type to the query if provided
            if room_type is not None:
                query = query.filter(Room.type == room_type)

            rooms = query.all()

            return [
                {
                    "number": room.number,
                    "type": room.type,
                    "max_guests": room.max_guests,
                    "description": room.description,
                    "amenities": room.amenities,
                    "price": room.price
                }
                for room in rooms
            ]
        except Exception as e:
            print(f'Error getting room details: {e}')
            return None
        finally:
            session.close()

    def get_rooms_by_type_and_city(self, room_type, city):
        session = self.get_session()
        try:
            query = (session.query(Room)
                     .join(Address)
                     .filter(Room.type == room_type, Address.city == city))

            rooms = query.all()

            return [
                {
                    "number": room.number,
                    "type": room.type,
                    "max_guests": room.max_guests,
                    "description": room.description,
                    "amenities": room.amenities,
                    "price": room.price
                }
                for room in rooms
            ]
        except Exception as e:
            print(f'Error getting room details: {e}')
            return None
        finally:
            session.close()


import logging
from pathlib import Path
import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, and_, not_, or_
from data_models.models import *
from data_access.data_base import init_db


class ReservationManager:
    def __init__(self, database_path: Path):
        """Initialize the ReservationManager class"""
        if not database_path.is_file():  # Checks if a DB file already exists
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get_session(self):
        return self.__session()

    def create_reservation(self, guest_id, room_hotel_id, room_number, number_of_guests, start_date, end_date,
                           comment=None):
        """Create a new reservation"""
        session = self.get_session()
        try:
            reservation = Booking(
                guest_id=guest_id,
                room_hotel_id=room_hotel_id,
                room_number=room_number,
                number_of_guests=number_of_guests,
                start_date=start_date,
                end_date=end_date,
                comment=comment
            )
            session.add(reservation)
            session.commit()
            return reservation
        except Exception as e:
            session.rollback()
            print(f'Error creating reservation: {e}')
            return None
        finally:
            session.close()

    def update_reservation(self, reservation_id, **kwargs):
        """Update an existing reservation"""
        session = self.get_session()
        try:
            reservation = session.query(Booking).filter(Booking.id == reservation_id).first()

            # If no reservation is found, return a meaningful message
            if not reservation:
                return 'No reservation found with the provided id'

            # Loop over the kwargs and update properties
            for key, value in kwargs.items():
                if hasattr(reservation, key):
                    setattr(reservation, key, value)
            session.commit()
            return 'Reservation successfully updated', reservation
        except Exception as e:
            session.rollback()
            logging.error(f'Error updating reservation: {e}')
            return f'Error occurred while updating reservation: {str(e)}'
        finally:
            session.close()

    def delete_reservation(self, reservation_id):
        """Delete an existing reservation"""
        session = self.get_session()
        try:
            reservation = session.query(Booking).filter(Booking.id == reservation_id).first()
            if not reservation:
                return False
            session.delete(reservation)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f'Error deleting reservation: {e}')
            return False
        finally:
            session.close()

    def get_reservation_details(self, reservation_id):
        """Get details of a specific reservation"""
        session = self.get_session()
        try:
            reservation = session.query(Booking).filter(Booking.id == reservation_id).first()
            if not reservation:
                return None
            return {
                'id': reservation.id,
                'guest': reservation.guest,
                'room': reservation.room,
                'number_of_guests': reservation.number_of_guests,
                'start_date': reservation.start_date,
                'end_date': reservation.end_date,
                'comment': reservation.comment
            }
        except Exception as e:
            print(f'Error getting reservation details: {e}')
            return None
        finally:
            session.close()

    def list_reservations(self, guest_id=None, room_hotel_id=None):
        """List all reservations, optionally filtered by guest or room"""
        session = self.get_session()
        try:
            query = session.query(Booking)
            if guest_id:
                query = query.filter(Booking.guest_id == guest_id)
            if room_hotel_id:
                query = query.filter(Booking.room_hotel_id == room_hotel_id)
            return query.all()
        except Exception as e:
            print(f'Error listing reservations: {e}')
            return None
        finally:
            session.close()

    def check_available_rooms(self, hotel_id, start_date, end_date):
        """Check available rooms in a hotel within a specified date range"""
        session = self.get_session()
        try:
            # Subquery to find rooms that are already booked within the date range
            subquery = session.query(Booking.room_number).filter(
                and_(
                    Booking.room_hotel_id == hotel_id,
                    not_(
                        or_(
                            Booking.end_date < start_date,
                            Booking.start_date > end_date
                        )
                    )
                )
            ).subquery()
            # Main query to find rooms that are not in the subquery
            available_rooms = session.query(Room).filter(
                and_(
                    Room.hotel_id == hotel_id,
                    Room.number.notin_(subquery)
                )
            ).all()
            return available_rooms
        except Exception as e:
            print(f'Error checking available rooms: {e}')
            return None
        finally:
            session.close()

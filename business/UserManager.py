import os

from pathlib import Path

from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from data_models.models import *
from console.console_base import *


from data_access.data_base import init_db


class UserManager(object):
    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get_session(self):
        return self.__session

    def ensure_superuser_created(self):
        """Create a superuser if it does not exist"""
        session = self.get_session()

        # If there's no user with role_id as 1, assume that superuser does not exist
        superuser = session.query(Login).filter_by(role_id=1).first()

        if not superuser:
            # Create a superuser with role_id as 1 and username as 'admin'
            superuser = Login(username="admin", password="admin", role_id=1)
            session.add(superuser)
            session.commit()
            print('Superuser created!'.format(superuser))
        else:
            print('Superuser already exists!')
        session.close()

    def create_new_login(self, email, password):
        """Creates a new login with provided email and password and sets role_id=2 auto"""
        session = self.get_session()
        existing_user = session.query(Login).filter_by(username=email).first()
        if existing_user:
            print("Email already exists. Please try again.")
            session.close()
            return False

        new_login = Login(username=email, password=password, role_id=2)
        session.add(new_login)
        session.commit()
        session.close()
        print("New login created successfully.")
        return True

    def register_existing_user(self, email, password):
        """adds additional guest details to an existing login"""
        session = self.get_session()
        user = session.query(Login).filter_by(username=email, password=password).first()
        if not user:
            print("Invalid email or password.")
            session.close()
            return False

        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        street = input("Enter street: ")
        zip_code = input("Enter zip code: ")
        city = input("Enter city: ")

        #print(f"Debug:" + street, zip_code, city)
        address = Address(street=street, zip=zip_code, city=city)
        session.add(address)
        session.commit()

        registered_guest = RegisteredGuest(
            firstname=first_name,
            lastname=last_name,
            email=email,
            address_id=address.id,
            login_id=user.id
        )

        session.add(registered_guest)
        session.commit()
        session.close()

        # address_id = address.id
        #
        # print(f"Debug:" + first_name, last_name, email, address_id)
        # guest = Guest(firstname=first_name, lastname=last_name, email=email, address_id=address_id, type='registered')
        # session.add(guest)
        # session.commit()

        # registered_guest = RegisteredGuest(login_id=user.id, id=guest.id)
        # session.add(registered_guest)
        # session.commit()
        # session.close()
        print("User registered successfully.")
        return True

    def authenticate_user(self, email, password):
        """Authenticate a user based on username and password."""
        # password hashing would be strongly advised - as discussed with lecturers and for simplicity's sake,
        # we will refrain from implementing this unless we have enough time to do so.
        # print("Authenticating user:", username, "with password:", password)  # debug what is getting passed into query
        session = self.get_session()
        user = session.query(Login).filter_by(username=email, password=password).first()
        if user:
            print(f"Login successful for {user.email}")
        if not user:
            print("Invalid email or password.")
            session.close()

    def create_guest(self, firstname, lastname, email, street, zip_code, city):
        """Create a new guest without login."""
        session = self.get_session()

        # Check if guest already exists
        existing_guest = session.query(Guest).filter_by(firstname=firstname, lastname=lastname, email=email).first()
        if existing_guest:
            print('Guest user already exists. Please try with a different name or email')
            session.close()
            return False

        address = Address(street=street, zip=zip_code, city=city)
        session.add(address)
        session.commit()

        new_guest = Guest(firstname=firstname, lastname=lastname, address=address, type='guest')
        session.add(new_guest)
        session.commit()
        session.close()
        print('New guest created successfully.')

    def authenticate_admin_user(self, email, password):
        """Authenticate a user based on username and password."""
        from console.console_base import HotelManagementConsole  # import only when needed

        session = self.get_session()
        user = session.query(Login).filter_by(and_(Login.username == email,
                                                   Login.password == password,
                                                   Login.role_id == 1)).first()
        session.close()

        if user:
            print(f"Login successful for {user.email}\nAdmin privileges granted. Navigating to hotel management console.")
            return HotelManagementConsole()
        else:
            print("Invalid email or password.")
            session.close()

import os
import hashlib
from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker
from data_access.data_base import init_db
from data_models.models import *

from data_access.our_db import init_our_db




class UserManager(object):
    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    #    def __load_db(self):
    #        db_filepath = Path(os.environ.get("DB_FILE", "../data/database.db"))
    #        if not db_filepath.is_file():
    #            init_db(str(db_filepath), generate_example_data=False)
    #        self._engine = create_engine(f'sqlite:///{db_filepath}')
    #        self._session = scoped_session(sessionmaker(bind=self._engine))

    def hash_password(self, password):
        """Hash a password for storing."""
        salt = os.urandom(16)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + pwdhash

    def register(self, username, password, role_name):
        """Register a new user."""
        session = self.__session()
        if session.query(User).filter_by(username=username).first():
            return False, "Username already exists."
        role = session.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
            session.commit()
        hashed_password = self.hash_password(password)
        new_user = User(username=username, password=hashed_password, role=role)
        session.add(new_user)
        session.commit()
        return True, "User registerd successfully."

    def login(self, username, password):
        """Login a user."""
        session = self.__session()
        user = session.query(User).filter_by(username=username).first()
        if user and self.check_password(user.password, password):
            return True, f"Login successful. Role: {user.role.name}"
        return False, "Invalid username or password."

    def check_password(self, hashed_password, user_password):
        """Verify a stored password against one provided by user."""
        salt = hashed_password[:16]
        stored_hash = hashed_password[16:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt, 100000)
        return pwdhash == stored_hash

    def check_reg_user(self, username, password):
        query = select(RegisteredGuest).join(Login).where(Login.username == username)
        result = self.__session.execute(query).scalars().one_or_none()
        print(result)
        if result:
            print("Registered User")
            if result.login.password == password:
                print("Login Successfull")
            else:
                print("Password or Username wrong")
        else:
            query_for_login = select(Login).where(Login.username == username)
            result = self.__session.execute(query_for_login).scalars().one_or_none()
            if result:
                print("None Guest Login")
                if result.password == password:
                    print("Login Successfull")
                    print(result.role.name)
                else:
                    print("Password or Username wrong")


if __name__ == "__main__":
    filepath = Path("../data/our_db.db")

    um = UserManager(filepath)
    um.check_reg_user("sabrina.schmidt@bluemail.ch", "SuperSecret")

    #print(um.register("admin", "hallo123", "admin"))
    #print(um.login("admin", "hallo123"))

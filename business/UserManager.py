import os
import hashlib
from pathlib import Path
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from data_access.data_base import init_db
from data_models.models import *

from data_access.data_base import init_db


class UserManager(object):
    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    # class UserManager(object):
    #     def __init__(self) -> None:
    #         self.__load_db()
    #
    #     def __load_db(self):
    #         if not os.environ.get("DB_FILE"):
    #             raise ValueError("You have to define the environment variable 'DB_FILE'")
    #         self.__db_filepath = Path(os.environ.get("DB_FILE"))
    #
    #         if not self.__db_filepath.is_file():
    #             init_db(str(self.__db_filepath), generate_example_data=True)
    #
    #         self._engine = create_engine(f'sqlite:///{self.__db_filepath}')
    #         self._session = scoped_session(sessionmaker(bind=self._engine))

    def register(self, username, password, role_name):
        """Register a new user."""
        session = self.__session()
        if session.query(Login).filter_by(username=username).first():
            return False, "Username already exists."
        role = session.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
            session.commit()
        new_user = Login(username=username, password=password, role=role)
        session.add(new_user)
        session.commit()
        return True, "User registerd successfully."

    # def register_user(self, email: str, password: str):
    #     new_user = Login(email=email, password=password)
    #     self.__session.add(new_user)
    #     self.__session.commit()
    #     return new_user

    def login(self, username: str, password: str):
        # password hashing would be strongly advised - as discussed with lecturers and for simplicitys sake, we will refrain from implementing this unless we have enough time to do so.
        # user = self.__session.execute(
        #     select(Login).where(and_(Guest.email == email, Login.password == password))
        # ).scalars().first()
        # return user
        user = self.__session.query(RegisteredGuest).join(Login).filter(Login.username == username,
                                                                        Login.password == password).first()
        if user:
            role_info = f' Role: {user.login.role.name}, Access Level: {user.login.role.access_level}'
            return f"User {username} logged in successfully.{role_info}"
        return "Invalid username or password."

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

    def close_session(self):
        self.__session.remove()


if __name__ == "__main__":
    filepath = Path("../data/my_db.db")

    um = UserManager(filepath)
    um.check_reg_user("sabrina.schmidt@bluemail.ch", "SuperSecret")

    um.login("sabrina.schmidt@bluemail", "SuperSecret")

    # print(um.register("admin", "hallo123", "admin"))
    # print(um.login("admin", "hallo123"))

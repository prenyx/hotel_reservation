import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from business.UserManager import UserManager
from data_access.data_base import init_db
from data_models import models
from data_models.models import Base, Guest, Login
from pathlib import Path


class Console(object):

    def __init__(self, database_path: Path):
        if not database_path.is_file():
            init_db(str(database_path), generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_path}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        self._database_path = database_path  # store the database_path as an instance variable

    def run(self):
        raise NotImplementedError("Implement this method")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')


class Application(object):

    def __init__(self, start: Console):
        self._current: Console = start

    def run(self):
        while self._current:
            self._current = self._current.run()


class MenuOption(object):
    def __init__(self, title):
        self._title = title

    def get_title(self) -> str:
        return self._title

    def __str__(self):
        return self._title

    def __len__(self):
        return len(self._title)


class Menu(Console):
    def __init__(self, title, database_path: Path, width=50):
        super().__init__(database_path)
        self._title = title
        self._options = []
        self._width = width

    def __iter__(self):
        return iter(self._options)

    def get_options(self) -> list:
        return self._options

    def add_option(self, option: MenuOption):
        self._options.append(option)

    def remove_option(self, option: MenuOption):
        self._options.remove(option)

    def _show(self):
        print("#" * self._width)
        left = "# "
        right = "#"
        space = " " * (self._width - len(left) - len(self._title) - len(right))
        print(f"{left}{self._title}{space}{right}")
        print("#" * self._width)
        for i, option in enumerate(self, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("#" * self._width)

    def _make_choice(self) -> int:
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            self._show()
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            console = UserRegistrationConsole(self._database_path)
            console.create_new_login()
            return console
        elif choice == 2:
            console = UserRegistrationConsole(self._database_path)
            console.register_existing_user()
            return console
        else:
            return self

    def run(self) -> Console:
        self.clear()
        self._show()
        return self._navigate(self._make_choice())


class UserRegistrationConsole(Console):
    def __init__(self, database_path: Path):
        super().__init__(database_path)
        self._user_manager = UserManager(database_path)

    def _navigate(self, choice: int) -> Optional[Console]:
        if choice == 1:
            self.create_new_login()
        elif choice == 2:
            self.register_existing_user()
        else:
            return None
        return self

    def create_new_login(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return
        self._user_manager.create_new_login(email, password)

    def register_existing_user(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        self._user_manager.register_existing_user(email, password)

    def run(self):
        menu = Menu("Hotel Reservation System", self._database_path)
        menu.add_option(MenuOption("Create New Login"))
        menu.add_option(MenuOption("Register Existing User"))
        return menu


if __name__ == "__main__":
    database_path = Path("../data/my_db.db")
    app = UserRegistrationConsole(database_path)
    # new_menu = app.run()
    # new_menu.run()
    # app.run()
    next_console = app.run()
    while next_console:
        next_console = next_console.run()

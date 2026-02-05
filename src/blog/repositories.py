import shelve
from abc import ABC, abstractmethod

from blog.domains import Admin, Item, Manager, User

class UsersRepository(ABC):
    """
    Абстрактный репозиторий для пользователей.
    От него нужно наследоваться в случае, когда нужно сделать другое хранилище, старое переписывать не нужно.
    """
    @abstractmethod
    def get_users(
        self, username: str | None = None, password: str | None = None
    ) -> list[User]:
        pass


class MemoryUsersRepository(UsersRepository):
    """
    Реализация пользовательского хранилища в оперативной памяти.
    Пользователи инициализируются во время инициализации репозитория
    """
    def __init__(self):
        self.users = [
            Admin(
                id="29ae7ebf-4445-42f2-9548-a3a54f095220",  # это uuid4 – уникальный идентификатор пользователя
                username="admin",
                password="Admin_4321!",
            ),
            Manager(
                id="29ae7ebf-4445-42f2-9548-a3a54f095221",  # это uuid4 – уникальный идентификатор пользователя
                username="manager",
                password="Manager_4321!",
            )
        ]

    def get_users(
        self, username: str | None = None, password: str | None = None
    ) -> list[User]:
        """
        :param username: фильтр по логину
        :param password: фильтр по паролю
        :return: отфильтрованные пользователи
        """
        filtered_users = []  # тут собираются отфильтрованные пользователи
        for user in self.users:  # перебираем всех пользователей и оставляем только тех, кто прошел фильтры
            if username is not None and user.username != username:
                continue
            if password is not None and user.password != password:
                continue
            filtered_users.append(user)
        return filtered_users


class ItemsRepository(ABC):
    """
    Абстрактный репозиторий для товаров.
    Он содержит методы, которые нужно реализовать в случае если захочется сделать новую реализацию репозитория.
    Принцип такой же как и у пользователей.
    """
    @abstractmethod
    def get_items(self) -> list[Item]:
        pass

    @abstractmethod
    def create_item(self, item: Item):
        pass

    @abstractmethod
    def update_item(self, item: Item):
        pass

class ShelveItemsRepository(ItemsRepository):
    def __init__(self):
        self.db_name = "Items"

    def get_items(self) -> list[Item]:
        with shelve.open(self.db_name) as db:
            return list(db.values())

    def create_item(self, item: Item):
        with shelve.open(self.db_name) as db:
            db[item.id] = item

    def update_item(self, item: Item):
        with shelve.open(self.db_name) as db:
            db[item.id] = item
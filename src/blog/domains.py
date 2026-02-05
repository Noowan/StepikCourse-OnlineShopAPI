from dataclasses import dataclass


@dataclass
class User:
    """Обычный пользователь"""
    id: str


@dataclass
class Admin(User):
    """Пользователь, наделенный правами администратора. Может всё, что может менеджер, а также добавлять товары на платформу"""
    username: str
    password: str

@dataclass
class Manager(User):
    """Пользователь, наделенный правами менеджера. Может менять товарам цену и описание"""
    username: str
    password: str

@dataclass
class Item:
    """Сущность товара, продаваемого в магазине"""
    id: str
    name: str
    description: str
    price: int
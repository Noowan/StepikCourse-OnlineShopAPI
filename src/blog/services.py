from uuid import uuid4

from blog.domains import Item, User
from blog.repositories import ItemsRepository, UsersRepository


def get_items(items_repository: ItemsRepository) -> list[Item]:
    return items_repository.get_items()


def create_item(name: str, description: str, price: int, items_repository: ItemsRepository) -> Item:
    item = Item(id=str(uuid4()),name=name, description=description, price=price)
    items_repository.create_item(item=item)
    return item


def update_item(id: str, name: str, description: str, price: int, items_repository: ItemsRepository) -> Item:
    item = Item(id=id, name=name, description=description, price=price)
    items_repository.update_item(item=item)
    return item


def login(
    username: str, password: str, users_repository: UsersRepository
) -> User | None:
    users = users_repository.get_users(username=username, password=password)
    if users:
        return users[0]
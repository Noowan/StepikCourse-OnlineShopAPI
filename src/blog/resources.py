from fastapi import APIRouter, status, HTTPException

from blog.domains import Admin, Manager
from blog.schemas import (
    GetItemsModel,
    CreateItemModel,
    LoginModel,
    GetItemModel,
    ErrorModel,
    UpdateItemModel
)
from blog import services
from blog.repositories import ShelveItemsRepository, MemoryUsersRepository

router = APIRouter()  # это роутер, он нужен для FastAPI, чтобы определять эндпоинты


@router.get("/items/get", response_model=GetItemsModel)
def get_items() -> GetItemsModel:
    # во всех представлениях всегда происходит одно и то же:
    # 1. получили данные
    # 2. вызвали сервисный метод и получили из него результат
    # 3. вернули результат клиенту в виде ответа
    items = services.get_items(items_repository=ShelveItemsRepository())
    return GetItemsModel(
        items=[
            GetItemModel(id=item.id, name=item.name, description=item.description, price=item.price)
            for item in items
        ]
    )


@router.post(
    "/items/create",
    response_model=GetItemModel,
    status_code=status.HTTP_201_CREATED,  # 201 статус код потому что мы создаем объект – стандарт HTTP
    responses={201: {"model": GetItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
)
def create_item(item: CreateItemModel,credentials: LoginModel):  # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        users_repository=MemoryUsersRepository(),
    )

    # Это аутентификация
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )
    # а это авторизация
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
        )

    item = services.create_item(
        name=item.name,
        description=item.description,
        price=item.price,
        items_repository=ShelveItemsRepository(),
    )

    return GetItemModel(id=item.id, name=item.name, description=item.description, price=item.price)

@router.post(
    "/items/update",
    response_model=UpdateItemModel,
    status_code=status.HTTP_201_CREATED,  # 201 статус код потому что мы создаем объект – стандарт HTTP
    responses={201: {"model": UpdateItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
)
def update_item(item: UpdateItemModel,credentials: LoginModel):  # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        users_repository=MemoryUsersRepository(),
    )

    # Это аутентификация
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )
    # а это авторизация
    if not (isinstance(current_user, Admin) or isinstance(current_user, Manager)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
        )

    item = services.update_item(
        id = item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        items_repository=ShelveItemsRepository(),
    )

    return GetItemModel(id=item.id, name=item.name, description=item.description, price=item.price)
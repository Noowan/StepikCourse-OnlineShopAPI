from pydantic import BaseModel


class GetItemModel(BaseModel):
    id: str
    name: str
    description: str
    price: int


class GetItemsModel(BaseModel):
    items: list[GetItemModel]


class CreateItemModel(BaseModel):
    name: str
    description: str
    price: int

class UpdateItemModel(BaseModel):
    id: str
    name: str
    description: str
    price: int

class LoginModel(BaseModel):
    username: str
    password: str


class ErrorModel(BaseModel):
    detail: str
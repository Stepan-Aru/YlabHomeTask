from typing import Optional

from pydantic import BaseModel


class BaseDataModel(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuModel(BaseDataModel):
    pass


class SubmenuModel(BaseDataModel):
    pass


class DishModel(BaseDataModel):
    price: float


class UpdateDataModel(BaseDataModel):
    title: Optional[str]
    description: Optional[str]


class UpdateMenuModel(UpdateDataModel):
    pass


class UpdateSubmenuModel(BaseDataModel):
    pass


class UpdateDishModel(BaseDataModel):
    price: Optional[float]


class ResponseDataModel(BaseDataModel):
    id: str


class ResponseMenuModel(ResponseDataModel):
    submenus_count: Optional[int]
    dishes_count: Optional[int]


class ResponseSubmenuModel(ResponseDataModel):
    dishes_count: Optional[int]


class ResponseDishModel(ResponseDataModel):
    price: str

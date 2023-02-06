from pydantic import BaseModel


class BaseDataModel(BaseModel):
    class Config:
        orm_mode = True


class MenuModel(BaseDataModel):
    title: str
    description: str


class SubmenuModel(BaseDataModel):
    title: str
    description: str


class DishModel(BaseDataModel):
    title: str
    description: str
    price: float


class UpdateMenuModel(BaseDataModel):
    title: str | None
    description: str | None


class UpdateSubmenuModel(BaseDataModel):
    title: str | None
    description: str | None


class UpdateDishModel(BaseDataModel):
    title: str | None
    description: str | None
    price: float | None


class ResponseMenuModel(BaseDataModel):
    id: str
    title: str
    description: str
    submenus_count: int | None
    dishes_count: int | None


class ResponseSubmenuModel(BaseDataModel):
    id: str
    title: str
    description: str
    dishes_count: int | None


class ResponseDishModel(BaseDataModel):
    id: str
    title: str
    description: str
    price: str

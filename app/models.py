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


class UpdateDataModel(BaseModel):
    title: str | None
    description: str | None

    class Config:
        orm_mode = True


class UpdateMenuModel(UpdateDataModel):
    pass


class UpdateSubmenuModel(BaseDataModel):
    pass


class UpdateDishModel(BaseDataModel):
    price: float | None


class ResponseDataModel(BaseDataModel):
    id: str


class ResponseMenuModel(ResponseDataModel):
    submenus_count: int | None
    dishes_count: int | None


class ResponseSubmenuModel(ResponseDataModel):
    dishes_count: int | None


class ResponseDishModel(ResponseDataModel):
    price: str

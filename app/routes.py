from fastapi import APIRouter, status, Depends

from app.database import create_tables

from app.models import (
    MenuModel,
    SubmenuModel,
    DishModel,
    UpdateMenuModel,
    UpdateSubmenuModel,
    UpdateDishModel,
    ResponseMenuModel,
    ResponseSubmenuModel,
    ResponseDishModel,
)
from app.services import (
    MenuService,
    get_menu_service,
    SubmenuService,
    get_submenu_service,
    DishService,
    get_dish_service,
)

router = APIRouter()


@router.on_event('startup')
async def startup():
    await create_tables()


@router.post(
    '/menus',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseMenuModel
)
async def create_menu_handler(
        menu: MenuModel,
        menu_service: MenuService = Depends(get_menu_service)
) -> ResponseMenuModel:
    return await menu_service.create_menu(menu=menu)


@router.post(
    '/menus/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSubmenuModel
)
async def create_submenu_handler(
        menu_id: int, submenu: SubmenuModel,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> ResponseSubmenuModel:
    return await submenu_service.create_submenu(menu_id=menu_id, submenu=submenu)


@router.post(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseDishModel
)
async def create_dish_handler(
        menu_id: int,
        submenu_id: int,
        dish: DishModel,
        dish_service: DishService = Depends(get_dish_service)
) -> ResponseDishModel:
    return await dish_service.create_dish(menu_id=menu_id, submenu_id=submenu_id, dish=dish)


@router.get(
    '/menus',
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseMenuModel]
)
async def get_menus_list_handler(
        menu_service: MenuService = Depends(get_menu_service)
) -> list[ResponseMenuModel]:
    return await menu_service.get_list()


@router.get(
    '/menus/{menu_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseMenuModel
)
async def get_menu_handler(
        menu_id: int,
        menu_service: MenuService = Depends(get_menu_service)
) -> ResponseMenuModel:
    return await menu_service.get_menu(menu_id=menu_id)


@router.get(
    '/menus/{menu_id}/submenus',
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseSubmenuModel]
)
async def get_submenus_list_handler(
        menu_id: int,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> list[ResponseSubmenuModel]:
    return await submenu_service.get_list(menu_id)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseSubmenuModel)
async def get_submenu_handler(
        menu_id: int,
        submenu_id: int,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> ResponseSubmenuModel:
    return await submenu_service.get_submenu(menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes',
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseDishModel]
)
async def get_dishes_list_handler(
        menu_id: int, submenu_id: int,
        dish_service: DishService = Depends(get_dish_service)
) -> list[ResponseDishModel]:
    return await dish_service.get_list(menu_id, submenu_id)


@router.get(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseDishModel
)
async def get_dish_handler(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish_service: DishService = Depends(get_dish_service)
) -> ResponseDishModel:
    return await dish_service.get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)


@router.patch(
    '/menus/{menu_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseMenuModel
)
async def update_menu_handler(
        menu_id: int,
        menu_update: UpdateMenuModel,
        menu_service: MenuService = Depends(get_menu_service)
) -> ResponseMenuModel:
    return await menu_service.update_menu(menu_update=menu_update, menu_id=menu_id)


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseSubmenuModel
)
async def update_submenu_handler(
        menu_id: int,
        submenu_id: int,
        submenu_update: UpdateSubmenuModel,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> ResponseSubmenuModel:
    return await submenu_service.update_submenu(menu_id=menu_id, submenu_id=submenu_id, submenu_update=submenu_update)


@router.patch(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseDishModel
)
async def update_dish_handler(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish_update: UpdateDishModel,
        dish_service: DishService = Depends(get_dish_service)
) -> ResponseDishModel:
    return await dish_service.update_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id,
                                          dish_update=dish_update)


@router.delete(
    '/menus/{menu_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseMenuModel
)
async def delete_menu_handler(
        menu_id: int,
        menu_service: MenuService = Depends(get_menu_service)
) -> ResponseMenuModel:
    return await menu_service.delete_menu(menu_id=menu_id)


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseSubmenuModel
)
async def delete_submenu_handler(
        menu_id: int,
        submenu_id: int,
        submenu_service: SubmenuService = Depends(get_submenu_service)
) -> ResponseSubmenuModel:
    return await submenu_service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)


@router.delete(
    '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseDishModel
)
async def delete_dish_handler(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish_service: DishService = Depends(get_dish_service)
) -> ResponseDishModel:
    return await dish_service.delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)

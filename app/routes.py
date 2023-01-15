from fastapi import APIRouter, status, HTTPException, Depends, Request

from sqlalchemy.orm import Session

from database import create_tables

from crud import (
    create_menu,
    create_submenu,
    create_dish,
    get_menus_list,
    get_menu,
    get_submenus_list,
    get_submenu,
    get_dishes_list,
    get_dish,
    update_menu,
    update_submenu,
    update_dish,
    delete_menu,
    delete_submenu,
    delete_dish,
)
from models import (
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

router = APIRouter()


def get_db(request: Request) -> Request:
    return request.state.db


async def is_item_created(item) -> None:
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


async def is_item_found(item, name: str) -> None:
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found")


@router.on_event('startup')
async def startup():
    await create_tables()


@router.post('/menus', status_code=status.HTTP_201_CREATED, response_model=ResponseMenuModel)
async def create_menu_handler(menu: MenuModel, db: Session = Depends(get_db)) -> ResponseMenuModel:
    new_menu = await create_menu(db, menu)
    await is_item_created(new_menu)
    return new_menu


@router.post('/menus/{menu_id}/submenus', status_code=status.HTTP_201_CREATED, response_model=ResponseSubmenuModel)
async def create_submenu_handler(menu_id: int, submenu: SubmenuModel,
                                 db: Session = Depends(get_db)) -> ResponseSubmenuModel:
    new_submenu = await create_submenu(db, submenu, menu_id)
    await is_item_created(new_submenu)
    return new_submenu


@router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=status.HTTP_201_CREATED,
             response_model=ResponseDishModel)
async def create_dish_handler(menu_id: int, submenu_id: int, dish: DishModel,
                              db: Session = Depends(get_db)) -> ResponseDishModel:
    new_dish = await create_dish(db, dish, menu_id, submenu_id)
    await is_item_created(new_dish)
    return new_dish


@router.get('/menus', status_code=status.HTTP_200_OK, response_model=list[ResponseMenuModel])
async def get_menus_list_handler(db: Session = Depends(get_db)) -> list[ResponseMenuModel]:
    return await get_menus_list(db)


@router.get('/menus/{menu_id}', status_code=status.HTTP_200_OK, response_model=ResponseMenuModel)
async def get_menu_handler(menu_id: int, db: Session = Depends(get_db)) -> ResponseMenuModel:
    menu = await get_menu(db, menu_id)
    await is_item_found(menu, 'menu')
    return menu


@router.get('/menus/{menu_id}/submenus', status_code=status.HTTP_200_OK, response_model=list[ResponseSubmenuModel])
async def get_submenus_list_handler(menu_id: int, db: Session = Depends(get_db)) -> list[ResponseSubmenuModel]:
    return await get_submenus_list(db, menu_id)


@router.get('/menus/{menu_id}/submenus/{submenu_id}', status_code=status.HTTP_200_OK,
            response_model=ResponseSubmenuModel)
async def get_submenu_handler(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> ResponseSubmenuModel:
    submenu = await get_submenu(db, menu_id, submenu_id)
    await is_item_found(submenu, 'submenu')
    return submenu


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes', status_code=status.HTTP_200_OK,
            response_model=list[ResponseDishModel])
async def get_dishes_list_handler(menu_id: int, submenu_id: int,
                                  db: Session = Depends(get_db)) -> list[ResponseDishModel]:
    return await get_dishes_list(db, menu_id, submenu_id)


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK,
            response_model=ResponseDishModel)
async def get_dish_handler(menu_id: int, submenu_id: int, dish_id: int,
                           db: Session = Depends(get_db)) -> ResponseMenuModel:
    dish = await get_dish(db, menu_id, submenu_id, dish_id)
    await is_item_found(dish, 'dish')
    return dish


@router.patch('/menus/{menu_id}', status_code=status.HTTP_200_OK, response_model=ResponseMenuModel)
async def update_menu_handler(menu_id: int, menu: UpdateMenuModel, db: Session = Depends(get_db)) -> ResponseMenuModel:
    updated_menu = await update_menu(db, menu, menu_id)
    await is_item_found(updated_menu, 'menu')
    return updated_menu


@router.patch('/menus/{menu_id}/submenus/{submenu_id}', status_code=status.HTTP_200_OK,
              response_model=ResponseSubmenuModel)
async def update_submenu_handler(menu_id: int, submenu_id: int, submenu: UpdateSubmenuModel,
                                 db: Session = Depends(get_db)) -> ResponseSubmenuModel:
    updated_submenu = await update_submenu(db, submenu, menu_id, submenu_id)
    await is_item_found(updated_submenu, 'submenu')
    return updated_submenu


@router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK,
              response_model=ResponseDishModel)
async def update_dish_handler(menu_id: int, submenu_id: int, dish_id: int, dish: UpdateDishModel,
                              db: Session = Depends(get_db)) -> ResponseDishModel:
    updated_dish = await update_dish(db, dish, menu_id, submenu_id, dish_id)
    await is_item_found(updated_dish, 'dish')
    return updated_dish


@router.delete('/menus/{menu_id}', status_code=status.HTTP_200_OK, response_model=ResponseMenuModel)
async def delete_menu_handler(menu_id: int, db: Session = Depends(get_db)) -> ResponseMenuModel:
    menu = await delete_menu(db, menu_id)
    await is_item_found(menu, 'menu')
    return menu


@router.delete('/menus/{menu_id}/submenus/{submenu_id}', status_code=status.HTTP_200_OK,
               response_model=ResponseSubmenuModel)
async def delete_submenu_handler(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> ResponseSubmenuModel:
    submenu = await delete_submenu(db, menu_id, submenu_id)
    await is_item_found(submenu, 'submenu')
    return submenu


@router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK,
               response_model=ResponseDishModel)
async def delete_dish_handler(menu_id: int, submenu_id: int, dish_id: int,
                              db: Session = Depends(get_db)) -> ResponseDishModel:
    dish = await delete_dish(db, menu_id, submenu_id, dish_id)
    await is_item_found(dish, 'dish')
    return dish

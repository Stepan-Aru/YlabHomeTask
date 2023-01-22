from sqlalchemy import func, distinct
from sqlalchemy.orm import Session

from app.database import Menu, Submenu, Dish

from app.models import (
    MenuModel,
    SubmenuModel,
    DishModel,
    UpdateMenuModel,
    UpdateSubmenuModel,
    UpdateDishModel,
)


async def create_menu(db: Session, menu: MenuModel) -> Menu:
    menu = Menu(**menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


async def create_submenu(db: Session, submenu: SubmenuModel, menu_id: int) -> Submenu:
    menu = await get_menu(db, menu_id)
    if menu:
        submenu = Submenu(**submenu.dict())
        menu.submenus.append(submenu)
        db.commit()
        db.refresh(submenu)
        return submenu


async def create_dish(db: Session, dish: DishModel, menu_id: int, submenu_id: int) -> Dish:
    submenu = await get_submenu(db, menu_id, submenu_id)
    if submenu:
        dish = Dish(**dish.dict())
        submenu.dishes.append(dish)
        db.commit()
        db.refresh(dish)
        return dish


async def add_counters_in_menu(item: tuple) -> Menu:
    menu = item[0]
    menu.submenus_count = item[1]
    menu.dishes_count = item[2]
    return menu


async def get_menus_list(db: Session) -> list[Menu]:
    query = db.query(
        Menu,
        func.count(distinct(Submenu.id)),
        func.count(Dish.id)
    ).join(
        Submenu,
        Menu.id == Submenu.menu_id,
        isouter=True
    ).join(
        Dish,
        Submenu.id == Dish.submenu_id,
        isouter=True
    ).group_by(Menu.id).all()
    return [await add_counters_in_menu(item) for item in query]


async def get_menu(db: Session, menu_id: int) -> Menu:
    query = db.query(
        Menu,
        func.count(distinct(Submenu.id)),
        func.count(Dish.id)
    ).join(
        Submenu,
        Menu.id == Submenu.menu_id,
        isouter=True
    ).join(
        Dish,
        Submenu.id == Dish.submenu_id,
        isouter=True
    ).filter(Menu.id == menu_id).group_by(Menu.id).first()
    return await add_counters_in_menu(query) if query else query


async def add_counter_in_submenu(item: tuple) -> Submenu:
    submenu = item[0]
    submenu.dishes_count = item[1]
    return submenu


async def get_submenus_list(db: Session, menu_id: int) -> list[Submenu]:
    query = db.query(
        Submenu,
        func.count(Dish.id)
    ).join(
        Dish,
        Submenu.id == Dish.submenu_id,
        isouter=True
    ).filter(Submenu.menu_id == menu_id).group_by(Submenu.id).all()
    return [await add_counter_in_submenu(item) for item in query]


async def get_submenu(db: Session, menu_id: int, submenu_id: int) -> Submenu:
    query = db.query(
        Submenu,
        func.count(Dish.id)
    ).join(
        Dish,
        Submenu.id == Dish.submenu_id,
        isouter=True
    ).filter(Submenu.menu_id == menu_id, Submenu.id == submenu_id).group_by(Submenu.id).first()
    return await add_counter_in_submenu(query) if query else query


async def get_dishes_list(db: Session, menu_id: int, submenu_id: int) -> list[Dish]:
    return db.query(Dish).join(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id).all()


async def get_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int) -> Dish:
    return db.query(Dish).join(Submenu).filter(Submenu.id == submenu_id,
                                               Submenu.menu_id == menu_id, Dish.id == dish_id).first()


async def update_menu(db: Session, menu_update: UpdateMenuModel, menu_id: int) -> Menu | None:
    menu = await get_menu(db, menu_id)
    menu.title = menu_update.title if menu_update.title else menu.title
    menu.description = menu_update.description if menu_update.description else menu.description
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


async def update_submenu(db: Session, submenu_update: UpdateSubmenuModel, menu_id: int, submenu_id: int) -> Submenu:
    submenu = await get_submenu(db, menu_id, submenu_id)
    submenu.title = submenu_update.title if submenu_update.title else submenu.title
    submenu.description = submenu_update.description if submenu_update.description else submenu.description
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


async def update_dish(db: Session, dish_update: UpdateDishModel, menu_id: int, submenu_id: int,
                      dish_id: int) -> Dish:
    dish = await get_dish(db, menu_id, submenu_id, dish_id)
    dish.title = dish_update.title if dish_update.title else dish.title
    dish.description = dish_update.description if dish_update.description else dish.description
    dish.price = dish_update.price if dish_update.price else dish.price
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


async def delete_menu(db: Session, menu_id: int) -> Menu:
    menu = await get_menu(db, menu_id)
    db.delete(menu)
    db.commit()
    return menu


async def delete_submenu(db: Session, menu_id: int, submenu_id: int) -> Submenu:
    submenu = await get_submenu(db, menu_id, submenu_id)
    db.delete(submenu)
    db.commit()
    return submenu


async def delete_dish(db: Session, menu_id: int, submenu_id: int, dish_id: int) -> Dish:
    dish = await get_dish(db, menu_id, submenu_id, dish_id)
    db.delete(dish)
    db.commit()
    return dish

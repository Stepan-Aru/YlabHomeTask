from sqlalchemy import distinct, func, select
from sqlalchemy.engine import Result, Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Dish, Menu, Submenu
from app.models import (
    DishModel,
    MenuModel,
    ResponseMenuModel,
    ResponseSubmenuModel,
    SubmenuModel,
    UpdateDishModel,
    UpdateMenuModel,
    UpdateSubmenuModel,
)


async def create_menu(db: AsyncSession, menu: MenuModel) -> Menu:
    menu = Menu(**menu.dict())
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def create_submenu(
    db: AsyncSession, submenu: SubmenuModel, menu_id: int
) -> Submenu | None:
    menu = await get_menu(db, menu_id)
    if menu:
        submenu = Submenu(**submenu.dict(), menu_id=menu_id)
        db.add(submenu)
        await db.commit()
        await db.refresh(submenu)
        return submenu
    return None


async def create_dish(
    db: AsyncSession, dish: DishModel, menu_id: int, submenu_id: int
) -> Dish | None:
    submenu = await get_submenu(db, menu_id, submenu_id)
    if submenu:
        dish = Dish(**dish.dict(), submenu_id=submenu_id)
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
        return dish
    return None


async def add_counters_in_menu(item: Row | Result) -> Menu:
    menu = item[0]
    menu.submenus_count = item[1]
    menu.dishes_count = item[2]
    return menu


async def get_menus_list(db: AsyncSession) -> list[ResponseMenuModel]:
    result = await db.execute(
        select(
            Menu,
            func.count(distinct(Submenu.id)),
            func.count(Dish.id),
        )
        .join(
            Submenu,
            Menu.id == Submenu.menu_id,
            isouter=True,
        )
        .join(
            Dish,
            Submenu.id == Dish.submenu_id,
            isouter=True,
        )
        .group_by(Menu.id),
    )
    return [await add_counters_in_menu(item) for item in result.all()]


async def get_menu(db: AsyncSession, menu_id: int) -> ResponseMenuModel:
    result = await db.execute(
        select(
            Menu,
            func.count(distinct(Submenu.id)),
            func.count(Dish.id),
        )
        .join(
            Submenu,
            Menu.id == Submenu.menu_id,
            isouter=True,
        )
        .join(
            Dish,
            Submenu.id == Dish.submenu_id,
            isouter=True,
        )
        .filter(Menu.id == menu_id)
        .group_by(Menu.id)
        .limit(1),
    )
    result = result.first()
    return await add_counters_in_menu(result) if result else result


async def add_counter_in_submenu(item: Row | Result) -> Submenu:
    submenu = item[0]
    submenu.dishes_count = item[1]
    return submenu


async def get_submenus_list(
    db: AsyncSession, menu_id: int
) -> list[ResponseSubmenuModel]:
    result = await db.execute(
        select(
            Submenu,
            func.count(Dish.id),
        )
        .join(
            Dish,
            Submenu.id == Dish.submenu_id,
            isouter=True,
        )
        .filter(Submenu.menu_id == menu_id)
        .group_by(Submenu.id),
    )
    return [await add_counter_in_submenu(item) for item in result.all()]


async def get_submenu(
    db: AsyncSession, menu_id: int, submenu_id: int
) -> ResponseSubmenuModel:
    result = await db.execute(
        select(
            Submenu,
            func.count(Dish.id),
        )
        .join(
            Dish,
            Submenu.id == Dish.submenu_id,
            isouter=True,
        )
        .filter(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
        .group_by(Submenu.id)
        .limit(1),
    )
    result = result.first()
    return await add_counter_in_submenu(result) if result else result


async def get_dishes_list(
    db: AsyncSession, menu_id: int, submenu_id: int
) -> list[Dish]:
    result = await db.execute(
        select(
            Dish,
        )
        .join(
            Submenu,
        )
        .filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id),
    )
    return result.scalars().all()


async def get_dish(
    db: AsyncSession, menu_id: int, submenu_id: int, dish_id: int
) -> Dish:
    result = await db.execute(
        select(
            Dish,
        )
        .join(
            Submenu,
        )
        .filter(
            Submenu.id == submenu_id,
            Submenu.menu_id == menu_id,
            Dish.id == dish_id,
        )
        .limit(1),
    )
    return result.scalar()


async def update_menu(
    db: AsyncSession,
    menu_update: UpdateMenuModel,
    menu_id: int,
) -> Menu:
    menu = await get_menu(db, menu_id)
    menu.title = menu_update.title if menu_update.title else menu.title
    menu.description = (
        menu_update.description if menu_update.description else menu.description
    )
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


async def update_submenu(
    db: AsyncSession,
    submenu_update: UpdateSubmenuModel,
    menu_id: int,
    submenu_id: int,
) -> Submenu:
    submenu = await get_submenu(db, menu_id, submenu_id)
    submenu.title = submenu_update.title if submenu_update.title else submenu.title
    submenu.description = (
        submenu_update.description
        if submenu_update.description
        else submenu.description
    )
    db.add(submenu)
    await db.commit()
    await db.refresh(submenu)
    return submenu


async def update_dish(
    db: AsyncSession,
    dish_update: UpdateDishModel,
    menu_id: int,
    submenu_id: int,
    dish_id: int,
) -> Dish:
    dish = await get_dish(db, menu_id, submenu_id, dish_id)
    dish.title = dish_update.title if dish_update.title else dish.title
    dish.description = (
        dish_update.description if dish_update.description else dish.description
    )
    dish.price = dish_update.price if dish_update.price else dish.price
    db.add(dish)
    await db.commit()
    await db.refresh(dish)
    return dish


async def delete_menu(db: AsyncSession, menu_id: int) -> Menu:
    menu = await get_menu(db, menu_id)
    await db.delete(menu)
    await db.commit()
    return menu


async def delete_submenu(db: AsyncSession, menu_id: int, submenu_id: int) -> Submenu:
    submenu = await get_submenu(db, menu_id, submenu_id)
    await db.delete(submenu)
    await db.commit()
    return submenu


async def delete_dish(
    db: AsyncSession, menu_id: int, submenu_id: int, dish_id: int
) -> Dish:
    dish = await get_dish(db, menu_id, submenu_id, dish_id)
    await db.delete(dish)
    await db.commit()
    return dish


async def get_all_data(db: AsyncSession):  # add type hinting
    result = await db.execute(
        select(Menu, Submenu, Dish)
        .join(
            Submenu,
            Menu.id == Submenu.menu_id,
            isouter=True,
        )
        .join(
            Dish,
            Submenu.id == Dish.submenu_id,
            isouter=True,
        )
    )
    return result.all()

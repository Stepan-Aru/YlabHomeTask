from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Dish, Menu, Submenu
from app.models import (
    DishModel,
    MenuModel,
    ResponseDishModel,
    ResponseMenuModel,
    ResponseSubmenuModel,
    SubmenuModel,
    UpdateDishModel,
    UpdateMenuModel,
    UpdateSubmenuModel,
)


async def create_menu(db: AsyncSession, menu: MenuModel) -> ResponseMenuModel:
    menu = Menu(**menu.dict())
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return ResponseMenuModel.from_orm(menu)


async def create_submenu(
    db: AsyncSession, submenu: SubmenuModel, menu_id: int
) -> ResponseSubmenuModel | None:
    menu = await get_menu(db, menu_id)
    if menu:
        submenu = Submenu(**submenu.dict(), menu_id=menu_id)
        db.add(submenu)
        await db.commit()
        await db.refresh(submenu)
        return ResponseSubmenuModel.from_orm(submenu)
    return None


async def create_dish(
    db: AsyncSession, dish: DishModel, menu_id: int, submenu_id: int
) -> ResponseDishModel | None:
    submenu = await get_submenu(db, menu_id, submenu_id)
    if submenu:
        dish = Dish(**dish.dict(), submenu_id=submenu_id)
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
        return ResponseDishModel.from_orm(dish)
    return None


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
    menus = []
    for row in result.all():
        menu = ResponseMenuModel.from_orm(row[0])
        menu.submenus_count = row[1]
        menu.dishes_count = row[2]
        menus.append(menu)
    return menus


async def get_menu(db: AsyncSession, menu_id: int) -> ResponseMenuModel | None:
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
    menu = None
    if result:
        menu = ResponseMenuModel.from_orm(result[0])
        menu.submenus_count = result[1]
        menu.dishes_count = result[2]
    return menu


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
    submenus = []
    for row in result.all():
        submenu = ResponseSubmenuModel.from_orm(row[0])
        submenu.dishes_count = row[1]
        submenus.append(submenu)
    return submenus


async def get_submenu(
    db: AsyncSession, menu_id: int, submenu_id: int
) -> ResponseSubmenuModel | None:
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
    submenu = None
    if result:
        submenu = ResponseSubmenuModel.from_orm(result[0])
        submenu.dishes_count = result[1]
    return submenu


async def get_dishes_list(
    db: AsyncSession, menu_id: int, submenu_id: int
) -> list[ResponseDishModel]:
    result = await db.execute(
        select(
            Dish,
        )
        .join(
            Submenu,
        )
        .filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id),
    )
    result = result.scalars().all()
    dishes = [ResponseDishModel.from_orm(row) for row in result]
    return dishes


async def get_dish(
    db: AsyncSession, menu_id: int, submenu_id: int, dish_id: int
) -> ResponseDishModel | None:
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
    result = result.scalar()
    dish = None
    if result:
        dish = ResponseDishModel.from_orm(result)
    return dish


async def update_menu(
    db: AsyncSession,
    menu_update: UpdateMenuModel,
    menu_id: int,
) -> ResponseMenuModel | None:
    menu = await db.execute(select(Menu).filter(Menu.id == menu_id).limit(1))
    menu = menu.scalar()
    if menu:
        menu.title = menu_update.title if menu_update.title else menu.title
        menu.description = (
            menu_update.description if menu_update.description else menu.description
        )
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
        return ResponseMenuModel.from_orm(menu)
    return None


async def update_submenu(
    db: AsyncSession,
    submenu_update: UpdateSubmenuModel,
    menu_id: int,
    submenu_id: int,
) -> ResponseSubmenuModel | None:
    submenu = await db.execute(
        select(Submenu)
        .filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
        .limit(1)
    )
    submenu = submenu.scalar()
    if submenu:
        submenu.title = submenu_update.title if submenu_update.title else submenu.title
        submenu.description = (
            submenu_update.description
            if submenu_update.description
            else submenu.description
        )
        db.add(submenu)
        await db.commit()
        await db.refresh(submenu)
        return ResponseSubmenuModel.from_orm(submenu)
    return None


async def update_dish(
    db: AsyncSession,
    dish_update: UpdateDishModel,
    menu_id: int,
    submenu_id: int,
    dish_id: int,
) -> ResponseDishModel | None:
    dish = await db.execute(
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
    dish = dish.scalar()
    if dish:
        dish.title = dish_update.title if dish_update.title else dish.title
        dish.description = (
            dish_update.description if dish_update.description else dish.description
        )
        dish.price = dish_update.price if dish_update.price else dish.price
        db.add(dish)
        await db.commit()
        await db.refresh(dish)
        return ResponseDishModel.from_orm(dish)
    return None


async def delete_menu(db: AsyncSession, menu_id: int) -> ResponseMenuModel | None:
    menu = await db.execute(select(Menu).filter(Menu.id == menu_id).limit(1))
    menu = menu.scalar()
    if menu:
        await db.delete(menu)
        await db.commit()
        return ResponseMenuModel.from_orm(menu)
    return None


async def delete_submenu(
    db: AsyncSession, menu_id: int, submenu_id: int
) -> ResponseSubmenuModel | None:
    submenu = await db.execute(
        select(Submenu)
        .filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
        .limit(1)
    )
    submenu = submenu.scalar()
    if submenu:
        await db.delete(submenu)
        await db.commit()
        return ResponseSubmenuModel.from_orm(submenu)
    return None


async def delete_dish(
    db: AsyncSession, menu_id: int, submenu_id: int, dish_id: int
) -> ResponseDishModel | None:
    dish = await db.execute(
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
    dish = dish.scalar()
    if dish:
        await db.delete(dish)
        await db.commit()
        return ResponseDishModel.from_orm(dish)
    return None


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

from dataclasses import dataclass

from fastapi import status, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app import crud
from app import cache

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


def get_db(request: Request) -> Request:
    return request.state.db


@dataclass
class Service:
    db: Session

    @staticmethod
    async def is_item_created(item) -> None:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request',
            )

    @staticmethod
    async def is_item_found(item, name: str) -> None:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'{name} not found',
            )


class MenuService(Service):
    @staticmethod
    async def update_cache(menu_id: int) -> None:
        await cache.delete_cache(
            names=(
                'menus_list',
                f'menu_{menu_id}',
            ),
        )

    async def create_menu(self, menu: MenuModel) -> ResponseMenuModel:
        new_menu = await crud.create_menu(db=self.db, menu=menu)
        await self.is_item_created(new_menu)
        await self.update_cache(menu_id=new_menu.id)
        return new_menu

    async def get_list(self) -> list[ResponseMenuModel]:
        menus_list = await cache.get_cache(name='menus_list')
        if not menus_list:
            menus_list = await crud.get_menus_list(db=self.db)
            await cache.set_cache(name='menus_list', value=menus_list)
        return menus_list

    async def get_menu(self, menu_id: int) -> ResponseMenuModel:
        menu = await cache.get_cache(name=f'menu_{menu_id}')
        if not menu:
            menu = await crud.get_menu(self.db, menu_id)
            await self.is_item_found(menu, 'menu')
            await cache.set_cache(name=f'menu_{menu_id}', value=menu)
        return menu

    async def update_menu(self, menu_update: UpdateMenuModel, menu_id: int) -> ResponseMenuModel:
        updated_menu = await crud.update_menu(db=self.db, menu_update=menu_update, menu_id=menu_id)
        await self.is_item_found(updated_menu, 'menu')
        await self.update_cache(menu_id=menu_id)
        return updated_menu

    async def delete_menu(self, menu_id: int) -> ResponseMenuModel:
        menu = await crud.delete_menu(db=self.db, menu_id=menu_id)
        await self.is_item_found(menu, 'menu')
        await self.update_cache(menu_id=menu_id)
        return menu


async def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    return MenuService(db)


class SubmenuService(Service):
    @staticmethod
    async def update_cache(menu_id: int, submenu_id: int) -> None:
        await cache.delete_cache(
            names=(
                'menus_list',
                f'menu_{menu_id}',
                f'submenus_list_{menu_id}',
                f'submenu_{menu_id}_{submenu_id}',
            ),
        )

    async def create_submenu(self, menu_id: int, submenu: SubmenuModel) -> ResponseSubmenuModel:
        new_submenu = await crud.create_submenu(db=self.db, menu_id=menu_id, submenu=submenu)
        await self.is_item_created(new_submenu)
        await self.update_cache(menu_id=menu_id, submenu_id=new_submenu.id)
        return new_submenu

    async def get_list(self, menu_id: int) -> list[ResponseSubmenuModel]:
        submenus_list = await cache.get_cache(name=f'submenus_list_{menu_id}')
        if not submenus_list:
            submenus_list = await crud.get_submenus_list(db=self.db, menu_id=menu_id)
            await cache.set_cache(name=f'submenus_list_{menu_id}', value=submenus_list)
        return submenus_list

    async def get_submenu(self, menu_id: int, submenu_id: int) -> ResponseSubmenuModel:
        submenu = await cache.get_cache(name=f'submenu_{menu_id}_{submenu_id}')
        if not submenu:
            submenu = await crud.get_submenu(db=self.db, menu_id=menu_id, submenu_id=submenu_id)
            await self.is_item_found(submenu, 'submenu')
            await cache.set_cache(name=f'submenu_{menu_id}_{submenu_id}', value=submenu)
        return submenu

    async def update_submenu(
            self,
            submenu_update: UpdateSubmenuModel,
            menu_id: int,
            submenu_id: int,
    ) -> ResponseSubmenuModel:
        updated_submenu = await crud.update_submenu(
            db=self.db,
            submenu_update=submenu_update,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        await self.is_item_found(updated_submenu, 'submenu')
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id)
        return updated_submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int) -> ResponseSubmenuModel:
        submenu = await crud.delete_submenu(db=self.db, menu_id=menu_id, submenu_id=submenu_id)
        await self.is_item_found(submenu, 'submenu')
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id)
        return submenu


async def get_submenu_service(db: Session = Depends(get_db)) -> SubmenuService:
    return SubmenuService(db)


class DishService(Service):
    @staticmethod
    async def update_cache(menu_id: int, submenu_id: int, dish_id: int) -> None:
        await cache.delete_cache(
            names=(
                'menus_list',
                f'menu_{menu_id}',
                f'submenus_list_{menu_id}',
                f'submenu_{menu_id}_{submenu_id}',
                f'dishes_list_{menu_id}_{submenu_id}',
                f'dish_{menu_id}_{submenu_id}_{dish_id}',
            ),
        )

    async def create_dish(self, menu_id: int, submenu_id: int, dish: DishModel) -> ResponseDishModel:
        new_dish = await crud.create_dish(db=self.db, menu_id=menu_id, submenu_id=submenu_id, dish=dish)
        await self.is_item_created(new_dish)
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=new_dish.id)
        return new_dish

    async def get_list(self, menu_id: int, submenu_id: int) -> list[ResponseDishModel]:
        dishes_list = await cache.get_cache(name=f'dishes_list_{menu_id}_{submenu_id}')
        if not dishes_list:
            dishes_list = await crud.get_dishes_list(db=self.db, menu_id=menu_id, submenu_id=submenu_id)
            await cache.set_cache(name=f'dishes_list_{menu_id}_{submenu_id}', value=dishes_list)
        return dishes_list

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> ResponseDishModel:
        dish = await cache.get_cache(name=f'dish_{menu_id}_{submenu_id}_{dish_id}')
        if not dish:
            dish = await crud.get_dish(db=self.db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
            await self.is_item_found(dish, 'dish')
            await cache.set_cache(name=f'dish_{menu_id}_{submenu_id}_{dish_id}', value=dish)
        return dish

    async def update_dish(
            self,
            dish_update: UpdateDishModel,
            menu_id: int,
            submenu_id: int,
            dish_id: int,
    ) -> ResponseDishModel:
        updated_dish = await crud.update_dish(
            db=self.db,
            dish_update=dish_update,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        await self.is_item_found(updated_dish, 'dish')
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return updated_dish

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> ResponseDishModel:
        dish = await crud.delete_dish(db=self.db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        await self.is_item_found(dish, 'dish')
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return dish


async def get_dish_service(db: Session = Depends(get_db)) -> DishService:
    return DishService(db)

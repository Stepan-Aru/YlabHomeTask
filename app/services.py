from dataclasses import dataclass

from celery.result import AsyncResult
from fastapi import Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import cache, crud
from app.celery_worker.tasks import data_report_task
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


def get_db(request: Request) -> Request:
    return request.state.db


@dataclass
class Service:
    db: AsyncSession

    @staticmethod
    async def is_item_created(item) -> HTTPException | bool:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad request",
            )
        return True

    @staticmethod
    async def is_item_found(item, name: str) -> HTTPException | bool:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{name} not found",
            )
        return True


class MenuService(Service):
    @staticmethod
    async def update_cache(menu_id: int | None = None) -> None:
        await cache.delete_cache(
            names=(
                "menus_list",
                f"menu_{menu_id}",
            ),
        )

    async def create_menu(self, menu: MenuModel) -> ResponseMenuModel | None:
        new_menu = await crud.create_menu(db=self.db, menu=menu)
        if await self.is_item_created(new_menu):
            await self.update_cache()
            return new_menu
        return None

    async def get_list(self) -> list[ResponseMenuModel]:
        menus_list = await cache.get_cache(name="menus_list")
        if not menus_list:
            menus_list = await crud.get_menus_list(db=self.db)
            await cache.set_cache(name="menus_list", value=menus_list)
        return menus_list

    async def get_menu(self, menu_id: int) -> ResponseMenuModel:
        menu = await cache.get_cache(name=f"menu_{menu_id}")
        if not menu:
            menu = await crud.get_menu(self.db, menu_id)
            await self.is_item_found(menu, "menu")
            await cache.set_cache(name=f"menu_{menu_id}", value=menu)
        return menu

    async def update_menu(
        self, menu_update: UpdateMenuModel, menu_id: int
    ) -> ResponseMenuModel | None:
        updated_menu = await crud.update_menu(
            db=self.db, menu_update=menu_update, menu_id=menu_id
        )
        await self.is_item_found(updated_menu, "menu")
        await self.update_cache(menu_id=menu_id)
        return updated_menu

    async def delete_menu(self, menu_id: int) -> ResponseMenuModel | None:
        menu = await crud.delete_menu(db=self.db, menu_id=menu_id)
        await self.is_item_found(menu, "menu")
        await self.update_cache(menu_id=menu_id)
        return menu


async def get_menu_service(db: AsyncSession = Depends(get_db)) -> MenuService:
    return MenuService(db=db)


class SubmenuService(Service):
    @staticmethod
    async def update_cache(menu_id: int, submenu_id: int | None = None) -> None:
        names = [
            "menus_list",
            f"menu_{menu_id}",
            f"submenus_list_{menu_id}",
        ]
        if submenu_id:
            names.append(f"submenu_{menu_id}_{submenu_id}")
        await cache.delete_cache(names=names)

    async def create_submenu(
        self, menu_id: int, submenu: SubmenuModel
    ) -> ResponseSubmenuModel | None:
        new_submenu = await crud.create_submenu(
            db=self.db, menu_id=menu_id, submenu=submenu
        )
        if await self.is_item_created(new_submenu):
            await self.update_cache(menu_id=menu_id)
            return new_submenu
        return None

    async def get_list(self, menu_id: int) -> list[ResponseSubmenuModel]:
        submenus_list = await cache.get_cache(name=f"submenus_list_{menu_id}")
        if not submenus_list:
            submenus_list = await crud.get_submenus_list(db=self.db, menu_id=menu_id)
            await cache.set_cache(name=f"submenus_list_{menu_id}", value=submenus_list)
        return submenus_list

    async def get_submenu(self, menu_id: int, submenu_id: int) -> ResponseSubmenuModel:
        submenu = await cache.get_cache(name=f"submenu_{menu_id}_{submenu_id}")
        if not submenu:
            submenu = await crud.get_submenu(
                db=self.db, menu_id=menu_id, submenu_id=submenu_id
            )
            await self.is_item_found(submenu, "submenu")
            await cache.set_cache(name=f"submenu_{menu_id}_{submenu_id}", value=submenu)
        return submenu

    async def update_submenu(
        self,
        submenu_update: UpdateSubmenuModel,
        menu_id: int,
        submenu_id: int,
    ) -> ResponseSubmenuModel | None:
        updated_submenu = await crud.update_submenu(
            db=self.db,
            submenu_update=submenu_update,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        await self.is_item_found(updated_submenu, "submenu")
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id)
        return updated_submenu

    async def delete_submenu(
        self, menu_id: int, submenu_id: int
    ) -> ResponseSubmenuModel | None:
        submenu = await crud.delete_submenu(
            db=self.db, menu_id=menu_id, submenu_id=submenu_id
        )
        await self.is_item_found(submenu, "submenu")
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id)
        return submenu


async def get_submenu_service(db: AsyncSession = Depends(get_db)) -> SubmenuService:
    return SubmenuService(db=db)


class DishService(Service):
    @staticmethod
    async def update_cache(
        menu_id: int, submenu_id: int, dish_id: int | None = None
    ) -> None:
        names = [
            "menus_list",
            f"menu_{menu_id}",
            f"submenus_list_{menu_id}",
            f"submenu_{menu_id}_{submenu_id}",
            f"dishes_list_{menu_id}_{submenu_id}",
        ]
        if dish_id:
            names.append(f"dish_{menu_id}_{submenu_id}_{dish_id}")
        await cache.delete_cache(names=names)

    async def create_dish(
        self, menu_id: int, submenu_id: int, dish: DishModel
    ) -> ResponseDishModel | None:
        new_dish = await crud.create_dish(
            db=self.db, menu_id=menu_id, submenu_id=submenu_id, dish=dish
        )
        if await self.is_item_created(new_dish):
            await self.update_cache(menu_id=menu_id, submenu_id=submenu_id)
            return new_dish
        return None

    async def get_list(self, menu_id: int, submenu_id: int) -> list[ResponseDishModel]:
        dishes_list = await cache.get_cache(name=f"dishes_list_{menu_id}_{submenu_id}")
        if not dishes_list:
            dishes_list = await crud.get_dishes_list(
                db=self.db, menu_id=menu_id, submenu_id=submenu_id
            )
            await cache.set_cache(
                name=f"dishes_list_{menu_id}_{submenu_id}", value=dishes_list
            )
        return dishes_list

    async def get_dish(
        self, menu_id: int, submenu_id: int, dish_id: int
    ) -> ResponseDishModel:
        dish = await cache.get_cache(name=f"dish_{menu_id}_{submenu_id}_{dish_id}")
        if not dish:
            dish = await crud.get_dish(
                db=self.db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
            )
            await self.is_item_found(dish, "dish")
            await cache.set_cache(
                name=f"dish_{menu_id}_{submenu_id}_{dish_id}", value=dish
            )
        return dish

    async def update_dish(
        self,
        dish_update: UpdateDishModel,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
    ) -> ResponseDishModel | None:
        updated_dish = await crud.update_dish(
            db=self.db,
            dish_update=dish_update,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        await self.is_item_found(updated_dish, "dish")
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return updated_dish

    async def delete_dish(
        self, menu_id: int, submenu_id: int, dish_id: int
    ) -> ResponseDishModel | None:
        dish = await crud.delete_dish(
            db=self.db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        )
        await self.is_item_found(dish, "dish")
        await self.update_cache(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return dish


async def get_dish_service(db: AsyncSession = Depends(get_db)) -> DishService:
    return DishService(db=db)


@dataclass
class DataReportService:
    db: AsyncSession

    async def create_data_report(self) -> dict:
        data = await crud.get_all_data(db=self.db)
        data = jsonable_encoder(data)
        task = data_report_task.delay(data)
        return {"task_id": task.id}

    @staticmethod
    async def get_data_report(task_id: str) -> FileResponse | dict:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            return FileResponse(
                path=task_result.result["path"],
                filename=task_result.result["file_name"],
                media_type="multipart/form-data",
            )
        else:
            return {
                "task_id": task_id,
                "task_status": task_result.status,
            }


async def get_data_report_service(
    db: AsyncSession = Depends(get_db),
) -> DataReportService:
    return DataReportService(
        db=db,
    )

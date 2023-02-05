from fastapi import APIRouter, Depends, status

from app.database import Dish, Menu, Submenu, create_tables
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
from app.services import (
    DataReportService,
    DishService,
    MenuService,
    SubmenuService,
    get_data_report_service,
    get_dish_service,
    get_menu_service,
    get_submenu_service,
)
from app.test_data.add_test_data import add_test_data

router = APIRouter()


@router.on_event("startup")
async def startup():
    await create_tables()


@router.post(
    path="/menus",
    tags=["Menu"],
    summary="Create menu",
    description="Create menu with title and description",
    response_description="Created menu",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseMenuModel,
)
async def create_menu_handler(
    menu: MenuModel,
    menu_service: MenuService = Depends(get_menu_service),
) -> Menu | None:
    return await menu_service.create_menu(menu=menu)


@router.post(
    path="/menus/{menu_id}/submenus",
    tags=["Submenu"],
    summary="Create submenu",
    description="Create submenu with title and description",
    response_description="Created submenu",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSubmenuModel,
)
async def create_submenu_handler(
    menu_id: int,
    submenu: SubmenuModel,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> Submenu | None:
    return await submenu_service.create_submenu(menu_id=menu_id, submenu=submenu)


@router.post(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dish"],
    summary="Create dish",
    description="Create dish with title, description and price",
    response_description="Created dish",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseDishModel,
)
async def create_dish_handler(
    menu_id: int,
    submenu_id: int,
    dish: DishModel,
    dish_service: DishService = Depends(get_dish_service),
) -> Dish | None:
    return await dish_service.create_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish=dish
    )


@router.get(
    path="/menus",
    tags=["Menu"],
    summary="Get menus list",
    description="Get menus list with title, description, submenus and dishes counters",
    response_description="Menus list",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseMenuModel],
)
async def get_menus_list_handler(
    menu_service: MenuService = Depends(get_menu_service),
) -> list[ResponseMenuModel]:
    return await menu_service.get_list()


@router.get(
    path="/menus/{menu_id}",
    tags=["Menu"],
    summary="Get menu",
    description="Get requested menu with title, description, submenus and dishes counters",
    response_description="Requested menu",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMenuModel,
)
async def get_menu_handler(
    menu_id: int,
    menu_service: MenuService = Depends(get_menu_service),
) -> ResponseMenuModel:
    return await menu_service.get_menu(menu_id=menu_id)


@router.get(
    path="/menus/{menu_id}/submenus",
    tags=["Submenu"],
    summary="Get submenus list",
    description="Get submenu list with title, description and dishes counter",
    response_description="Submenu list",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseSubmenuModel],
)
async def get_submenus_list_handler(
    menu_id: int,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> list[ResponseSubmenuModel]:
    return await submenu_service.get_list(menu_id)


@router.get(
    path="/menus/{menu_id}/submenus/{submenu_id}",
    tags=["Submenu"],
    summary="Get submenu",
    description="Get requested submenu with title, description and dishes counter",
    response_description="Requested submenu",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSubmenuModel,
)
async def get_submenu_handler(
    menu_id: int,
    submenu_id: int,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> ResponseSubmenuModel:
    return await submenu_service.get_submenu(menu_id=menu_id, submenu_id=submenu_id)


@router.get(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dish"],
    summary="Get dishes list",
    description="Get dishes list with title, description and price",
    response_description="Dishes list",
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseDishModel],
)
async def get_dishes_list_handler(
    menu_id: int,
    submenu_id: int,
    dish_service: DishService = Depends(get_dish_service),
) -> list[ResponseDishModel]:
    return await dish_service.get_list(menu_id, submenu_id)


@router.get(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    tags=["Dish"],
    summary="Get dish",
    description="Get requested dish with title, description and price",
    response_description="Requested dish",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDishModel,
)
async def get_dish_handler(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish_service: DishService = Depends(get_dish_service),
) -> ResponseDishModel:
    return await dish_service.get_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )


@router.patch(
    path="/menus/{menu_id}",
    tags=["Menu"],
    summary="Update menu",
    description="Update menu information: title and description",
    response_description="Updated menu",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMenuModel,
)
async def update_menu_handler(
    menu_id: int,
    menu_update: UpdateMenuModel,
    menu_service: MenuService = Depends(get_menu_service),
) -> Menu | None:
    return await menu_service.update_menu(menu_update=menu_update, menu_id=menu_id)


@router.patch(
    path="/menus/{menu_id}/submenus/{submenu_id}",
    tags=["Submenu"],
    summary="Update submenu",
    description="Update submenu information: title and description",
    response_description="Updated submenu",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSubmenuModel,
)
async def update_submenu_handler(
    menu_id: int,
    submenu_id: int,
    submenu_update: UpdateSubmenuModel,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> Submenu | None:
    return await submenu_service.update_submenu(
        menu_id=menu_id, submenu_id=submenu_id, submenu_update=submenu_update
    )


@router.patch(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    tags=["Dish"],
    summary="Update dish",
    description="Update dish information: title, description and price",
    response_description="Updated dish",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDishModel,
)
async def update_dish_handler(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish_update: UpdateDishModel,
    dish_service: DishService = Depends(get_dish_service),
) -> Dish | None:
    return await dish_service.update_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
        dish_update=dish_update,
    )


@router.delete(
    path="/menus/{menu_id}",
    tags=["Menu"],
    summary="Delete menu",
    description="Delete requested menu with all submenus and dishes",
    response_description="Deleted menu",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMenuModel,
)
async def delete_menu_handler(
    menu_id: int,
    menu_service: MenuService = Depends(get_menu_service),
) -> ResponseMenuModel:
    return await menu_service.delete_menu(menu_id=menu_id)


@router.delete(
    path="/menus/{menu_id}/submenus/{submenu_id}",
    tags=["Submenu"],
    summary="Delete submenu",
    description="Delete requested submenu with all dishes",
    response_description="Deleted submenu",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSubmenuModel,
)
async def delete_submenu_handler(
    menu_id: int,
    submenu_id: int,
    submenu_service: SubmenuService = Depends(get_submenu_service),
) -> ResponseSubmenuModel:
    return await submenu_service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)


@router.delete(
    path="/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    tags=["Dish"],
    summary="Delete dish",
    description="Delete requested dish",
    response_description="Deleted dish",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDishModel,
)
async def delete_dish_handler(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish_service: DishService = Depends(get_dish_service),
) -> ResponseDishModel:
    return await dish_service.delete_dish(
        menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
    )


@router.post(
    path="/data_report/add_test_data",
    tags=["Data report"],
    summary="Add test data",
    description="Add test data in database",
    response_description="Test data added in database",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
)
async def add_test_data_handler(
    menu_service: MenuService = Depends(get_menu_service),
    submenu_service: SubmenuService = Depends(get_submenu_service),
    dishes_service: DishService = Depends(get_dish_service),
) -> str:
    return await add_test_data(
        menu_service=menu_service,
        submenu_service=submenu_service,
        dishes_service=dishes_service,
    )


@router.post(
    path="/data_report",
    tags=["Data report"],
    summary="Create data report",
    description="Create a data report generation task",
    response_description="Data report generation task created",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_data_report_handler(
    data_report_service: DataReportService = Depends(get_data_report_service),
) -> dict:
    return await data_report_service.create_data_report()


@router.get(
    path="/data_report/{task_id}",
    tags=["Data report"],
    summary="Get data report",
    description="Get result of data report generation task",
    response_description="Result of data report generation task",
    status_code=status.HTTP_200_OK,
)
async def get_data_report_handler(
    task_id: str,
    data_report_service: DataReportService = Depends(get_data_report_service),
):
    return await data_report_service.get_data_report(task_id=task_id)

import json
from pathlib import Path

from app.models import DishModel, MenuModel, SubmenuModel
from app.services import DishService, MenuService, SubmenuService


async def read_test_data_from_json() -> list:
    with open(Path("app", "test_data", "test_data.json")) as file:
        return json.loads(file.read())["data"]


async def add_test_data(
    menu_service: MenuService,
    submenu_service: SubmenuService,
    dishes_service: DishService,
) -> str:
    data = await read_test_data_from_json()
    for menu_data in data:
        menu = MenuModel.parse_obj(
            {
                "title": menu_data["title"],
                "description": menu_data["description"],
            }
        )
        new_menu = await menu_service.create_menu(menu)
        if new_menu:
            for submenu_data in menu_data["submenus"]:
                submenu = SubmenuModel.parse_obj(
                    {
                        "title": submenu_data["title"],
                        "description": submenu_data["description"],
                    }
                )
                new_submenu = await submenu_service.create_submenu(
                    submenu=submenu, menu_id=new_menu.id
                )
                if new_submenu:
                    for dish_data in submenu_data["dishes"]:
                        dish = DishModel.parse_obj(
                            {
                                "title": dish_data["title"],
                                "description": dish_data["description"],
                                "price": dish_data["price"],
                            }
                        )
                        await dishes_service.create_dish(
                            dish=dish,
                            menu_id=new_menu.id,
                            submenu_id=new_submenu.id,
                        )
    return "Test data added successfully"

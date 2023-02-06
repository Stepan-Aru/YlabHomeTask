from pathlib import Path

from xlsxwriter import Workbook


def write_xlsx_file(data: dict, file_path: Path) -> None:
    workbook = None
    try:
        workbook = Workbook(file_path)
        worksheet = workbook.add_worksheet()
        worksheet.set_column("A:A", 5)
        worksheet.set_column("B:B", 7)
        worksheet.set_column("C:D", 20)
        worksheet.set_column("E:E", 50)
        worksheet.set_column("F:F", 10)
        bold = workbook.add_format({"bold": True})
        row = 0
        for menu_num, menu in enumerate(data.values()):
            worksheet.write(row, 0, menu_num + 1, bold)
            worksheet.write(row, 1, menu["title"], bold)
            worksheet.write(row, 2, menu["description"], bold)
            row += 1
            for submenu_num, submenu in enumerate(menu["submenus"].values()):
                worksheet.write(row, 1, submenu_num + 1, bold)
                worksheet.write(row, 2, submenu["title"], bold)
                worksheet.write(row, 3, submenu["description"], bold)
                row += 1
                for dish_num, dish in enumerate(submenu["dishes"].values()):
                    worksheet.write(row, 2, dish_num + 1)
                    worksheet.write(row, 3, dish["title"], bold)
                    worksheet.write(row, 4, dish["description"], bold)
                    worksheet.write(row, 5, dish["price"], bold)
                    row += 1
    except Exception as ex:
        print(ex)
    finally:
        if workbook:
            workbook.close()


def data_parser(data: list) -> dict:
    result_data = {}
    for row in data:
        menu = row["Menu"]
        menu_id = menu["id"]
        if menu_id not in result_data:
            result_data[menu_id] = {
                "title": menu["title"],
                "description": menu["description"],
                "submenus": {},
            }
        if row["Submenu"]:
            submenu = row["Submenu"]
            submenu_id = submenu["id"]
            if submenu_id not in result_data[menu_id]["submenus"]:
                result_data[menu_id]["submenus"][submenu_id] = {
                    "title": submenu["title"],
                    "description": submenu["description"],
                    "dishes": {},
                }
            if row["Dish"]:
                dish = row["Dish"]
                dish_id = dish["id"]
                if (
                    dish_id
                    not in result_data[menu_id]["submenus"][submenu_id]["dishes"]
                ):
                    result_data[menu_id]["submenus"][submenu_id]["dishes"][dish_id] = {
                        "title": dish["title"],
                        "description": dish["description"],
                        "price": dish["price"],
                    }
    return result_data

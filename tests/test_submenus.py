import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_submenus_post_menu(async_client: AsyncClient):
    response = await async_client.post(
        "api/v1/menus",
        json={
            "title": "My menu 1",
            "description": "My menu description 1",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": None,
        "dishes_count": None,
    }


@pytest.mark.asyncio
async def test_submenus_get_submenu_list_empty(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus/1/submenus")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_submenus_post_submenu(async_client: AsyncClient):
    response = await async_client.post(
        "api/v1/menus/1/submenus",
        json={
            "title": "My submenu 1",
            "description": "My submenu description 1",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": "1",
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": None,
    }


@pytest.mark.asyncio
async def test_submenus_get_submenu_list(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus/1/submenus")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [
        {
            "id": "1",
            "title": "My submenu 1",
            "description": "My submenu description 1",
            "dishes_count": 0,
        }
    ]


@pytest.mark.asyncio
async def test_submenus_get_submenu(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus/1/submenus/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 0,
    }


@pytest.mark.asyncio
async def test_submenus_patch_submenu(async_client: AsyncClient):
    response = await async_client.patch(
        "api/v1/menus/1/submenus/1",
        json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
        "dishes_count": None,
    }


@pytest.mark.asyncio
async def test_submenus_get_updated_submenu(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus/1/submenus/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
        "dishes_count": 0,
    }


@pytest.mark.asyncio
async def test_submenus_delete_submenu(async_client: AsyncClient):
    response = await async_client.delete("api/v1/menus/1/submenus/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
        "dishes_count": None,
    }


@pytest.mark.asyncio
async def test_submenus_get_submenu_list_after_delete(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus/1/submenus")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_submenus_get_submenu_not_found(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus/1/submenus/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


@pytest.mark.asyncio
async def test_submenus_delete_menu(async_client: AsyncClient):
    response = await async_client.delete("api/v1/menus/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": None,
        "dishes_count": None,
    }


@pytest.mark.asyncio
async def test_submenus_get_menu_list_after_delete(async_client: AsyncClient):
    response = await async_client.get("api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []

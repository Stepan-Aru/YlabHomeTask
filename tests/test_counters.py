import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_counters_post_menu(async_client: AsyncClient):
    response = await async_client.post('api/v1/menus', json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert response.status_code == 201
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": None,
        "dishes_count": None
    }


@pytest.mark.asyncio
async def test_counters_post_submenu(async_client: AsyncClient):
    response = await async_client.post('api/v1/menus/1/submenus', json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert response.status_code == 201
    assert response.json() == {
        "id": "1",
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": None
    }


@pytest.mark.asyncio
async def test_counters_post_dish_1(async_client: AsyncClient):
    response = await async_client.post('api/v1/menus/1/submenus/1/dishes', json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "13.50"
    })
    assert response.status_code == 201
    assert response.json() == {
        "id": "1",
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "13.50"
    }


@pytest.mark.asyncio
async def test_counters_post_dish_2(async_client: AsyncClient):
    response = await async_client.post('api/v1/menus/1/submenus/1/dishes', json={
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "12.50"
    })
    assert response.status_code == 201
    assert response.json() == {
        "id": "2",
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "12.50"
    }


@pytest.mark.asyncio
async def test_counters_get_menu(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 1,
        "dishes_count": 2
    }


@pytest.mark.asyncio
async def test_counters_get_submenu(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1/submenus/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 2
    }


@pytest.mark.asyncio
async def test_counters_delete_submenu(async_client: AsyncClient):
    response = await async_client.delete('api/v1/menus/1/submenus/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 2
    }


@pytest.mark.asyncio
async def test_counters_get_submenu_list_after_delete(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1/submenus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_counters_get_dishes_list_after_delete(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1/submenus/1/dishes')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_counters_get_menu_after_delete_submenu(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }


@pytest.mark.asyncio
async def test_counters_delete_menu(async_client: AsyncClient):
    response = await async_client.delete('api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }


@pytest.mark.asyncio
async def test_counters_get_menu_list_after_delete(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_menus_get_menu_list_empty(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_menus_post_menu(async_client: AsyncClient):
    response = await async_client.post(
        'api/v1/menus', json={
            'title': 'My menu 1',
            'description': 'My menu description 1',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'id': '1',
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': None,
        'dishes_count': None,
    }


@pytest.mark.asyncio
async def test_menus_get_menu_list(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus')
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [{
        'id': '1',
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }]


@pytest.mark.asyncio
async def test_menus_get_menu(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        'id': '1',
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }


@pytest.mark.asyncio
async def test_menus_patch_menu(async_client: AsyncClient):
    response = await async_client.patch(
        'api/v1/menus/1', json={
            'title': 'My updated menu 1',
            'description': 'My updated menu description 1',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': '1',
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }


@pytest.mark.asyncio
async def test_menus_get_updated_menu(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        'id': '1',
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }


@pytest.mark.asyncio
async def test_menus_delete_menu(async_client: AsyncClient):
    response = await async_client.delete('api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        'id': '1',
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
        'submenus_count': 0,
        'dishes_count': 0,
    }


@pytest.mark.asyncio
async def test_menus_get_menu_list_after_delete(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_menus_get_menu_not_found(async_client: AsyncClient):
    response = await async_client.get('api/v1/menus/1')
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}

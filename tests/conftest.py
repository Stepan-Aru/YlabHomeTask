import asyncio
import os
from typing import Generator

import asyncpg
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app
from app.services import get_db

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME')


async def execute_db(command: str):
    conn = None
    try:
        conn = await asyncpg.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_URL,
        )
        await conn.execute(command)
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()


async def create_test_db():
    await execute_db(f'CREATE DATABASE test_{DB_NAME};')


async def drop_test_db():
    await execute_db(f'DROP DATABASE IF EXISTS test_{DB_NAME};')


async def kill_all_connections():
    await execute_db(
        f'SELECT pg_terminate_backend(pg_stat_activity.pid)\n'
        f'FROM pg_stat_activity\n'
        f'WHERE pg_stat_activity.datname = \'test_{DB_NAME}\'\n'
        f'AND pid <> pg_backend_pid();',
    )


async def create_test_session_local():
    TEST_DB_CONFIG = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_URL}/test_{DB_NAME}'
    test_engine = create_async_engine(TEST_DB_CONFIG, echo=True)
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_db():
        db = None
        try:
            db = TestSessionLocal()
            yield db
        finally:
            await db.close()

    app.dependency_overrides[get_db] = override_get_db
    await create_tables(test_engine)


async def create_tables(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module', autouse=True)
async def create_drop_database():
    await create_test_db()
    await create_test_session_local()
    yield
    await kill_all_connections()
    await drop_test_db()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac

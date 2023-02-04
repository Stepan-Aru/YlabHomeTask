import asyncio
import os
from typing import Generator

import asyncpg
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, session

from app.database import Base
from app.main import app
from app.services import get_db

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME')


def execute_db(command: str):
    conn = None
    try:
        conn = await asyncpg.connect(
            database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_URL,
        )
        conn.autocommit = True
        await conn.execute(command)
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()


def create_test_db():
    execute_db(f'CREATE DATABASE test_{DB_NAME};')


def drop_test_db():
    execute_db(f'DROP DATABASE IF EXISTS test_{DB_NAME};')


def kill_all_connections():
    execute_db(
        f'SELECT pg_terminate_backend(pg_stat_activity.pid)\n'
        f'FROM pg_stat_activity\n'
        f'WHERE pg_stat_activity.datname = \'test_{DB_NAME}\'\n'
        f'AND pid <> pg_backend_pid();',
    )


def create_test_session_local():
    TEST_DB_CONFIG = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_URL}/test_{DB_NAME}'
    test_engine = create_async_engine(TEST_DB_CONFIG, echo=True)
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    def override_get_db():
        db = None
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='module', autouse=True)
def create_drop_database():
    create_test_db()
    create_test_session_local()
    yield
    session.close_all_sessions()
    kill_all_connections()
    drop_test_db()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac

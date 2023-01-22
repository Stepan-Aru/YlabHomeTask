import os

import psycopg2
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session

from app.database import Base
from app.main import app
from app.routes import get_db

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME')


def execute_db(command: str):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_URL)
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(command)
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        conn.close()


def create_test_db():
    execute_db(f"CREATE DATABASE test_{DB_NAME};")


def drop_test_db():
    execute_db(f"DROP DATABASE IF EXISTS test_{DB_NAME};")


def kill_all_connections():
    execute_db(f"SELECT pg_terminate_backend(pg_stat_activity.pid)\n"
               f"FROM pg_stat_activity\n"
               f"WHERE pg_stat_activity.datname = 'test_{DB_NAME}'\n"
               f"AND pid <> pg_backend_pid();")


def create_test_session_local():
    TEST_DB_CONFIG = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_URL}/test_{DB_NAME}"
    test_engine = create_engine(TEST_DB_CONFIG)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="module", autouse=True)
def create_drop_database():
    create_test_db()
    create_test_session_local()
    yield
    session.close_all_sessions()
    kill_all_connections()
    drop_test_db()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

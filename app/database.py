import os

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    DeclarativeMeta,
    backref,
    declarative_base,
    relationship,
    sessionmaker,
)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")

DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"

engine = create_async_engine(DB_CONFIG, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base: DeclarativeMeta = declarative_base()


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    menu_id = Column(Integer(), ForeignKey("menus.id"))
    menu = relationship(
        "Menu",
        backref=backref(
            "submenus",
            cascade="all,delete",
        ),
        foreign_keys=[menu_id],
    )


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    submenu_id = Column(Integer(), ForeignKey("submenus.id"))
    submenu = relationship(
        "Submenu",
        backref=backref(
            "dishes",
            cascade="all,delete",
        ),
        foreign_keys=[submenu_id],
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME')

DB_CONFIG = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"

engine = create_engine(DB_CONFIG, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseTable:
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=False)


class Menu(BaseTable, Base):
    __tablename__ = 'menus'


class Submenu(BaseTable, Base):
    __tablename__ = 'submenus'

    menu_id = Column(Integer(), ForeignKey('menus.id'))
    menu = relationship('Menu', backref=backref("submenus", cascade="all,delete"), foreign_keys=[menu_id])


class Dish(BaseTable, Base):
    __tablename__ = 'dishes'

    price = Column(Numeric(10, 2), nullable=False)
    submenu_id = Column(Integer(), ForeignKey('submenus.id'))
    submenu = relationship('Submenu', backref=backref("dishes", cascade="all,delete"), foreign_keys=[submenu_id])


async def create_tables():
    Base.metadata.create_all(engine)

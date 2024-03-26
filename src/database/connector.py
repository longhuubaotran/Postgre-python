from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URL
from .models import Base

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionDB = sessionmaker(engine)


def initilizeTables():
    Base.metadata.create_all(engine)

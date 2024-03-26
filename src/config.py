import os
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv(override=True)

SQLALCHEMY_DATABASE_URL = URL.create(
    os.getenv("DATABASE_URL"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST_DOMAIN"),
    database=os.getenv("DATABASE_NAME"),
)

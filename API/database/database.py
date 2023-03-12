from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

if os.environ.get('ENV_TYPE') == "DEVELOPMENT":

    user_name = os.environ.get("MYSQL_USER")
    user_password = os.environ.get("MYSQL_PASSWORD")
    mysql_host = os.environ.get("MYSQL_HOST")
    mysql_port = int(os.environ.get('MYSQL_PORT'))
    database_name = os.environ.get("MYSQL_DATABASE")
else:
    user_name = os.environ.get("MYSQL_USER")
    user_password = os.environ.get("MYSQL_PASSWORD")
    mysql_port = int(os.environ.get("MYSQL_PORT"))
    mysql_host = os.environ.get("MYSQL-SERVICE-HOST")
    database_name = os.environ.get("MYSQL_DATABASE")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user_name}:{user_password}@{mysql_url}:3306/{database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
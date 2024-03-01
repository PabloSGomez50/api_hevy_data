from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv(override=True)
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_PORT = os.getenv("DATABASE_PORT", 3306)
DATABASE_IP = os.getenv("DATABASE_IP", "localhost")

class Base(DeclarativeBase):
    pass
# Base = declarative_base()
db_type = os.getenv("DATABASE_TYPE", 'sqlite')

connect_args = {}
if db_type == "mysql":
    conn_url = "mysql+pymysql://{}:{}@{}:{}/{}".format(
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_IP,
        DATABASE_PORT,
        DATABASE_DB
    )
elif db_type == 'sqlite':
    conn_url = "sqlite:///./app.db"
    connect_args["check_same_thread"] = False
# print(conn_url)
engine = create_engine(conn_url, connect_args=connect_args)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    """
    Retrieve db session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
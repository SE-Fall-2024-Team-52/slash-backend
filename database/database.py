from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# postgres connection
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
SQLALCHEMY_DATABASE_URL = (
    "postgresql://" + username + ":" + password + "@localhost/slash"
)
# SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()

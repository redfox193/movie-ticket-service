import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

if os.getenv('POSTGRES_HOST') is None:
    dotenv_path = os.path.join(os.path.dirname(__file__), '../../../.env')
    load_dotenv(dotenv_path=dotenv_path)
    POSTGRES_HOST = "localhost"
else:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')

DB_URL = (f"postgresql+psycopg2://"
          f"{os.getenv('POSTGRES_USER')}:"
          f"{os.getenv('POSTGRES_PASSWORD')}@"
          f"{POSTGRES_HOST}:"
          f"{os.getenv('POSTGRES_PORT')}/"
          f"{os.getenv('POSTGRES_DB')}")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

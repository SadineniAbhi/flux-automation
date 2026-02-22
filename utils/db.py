import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlmodel import Session
from models import project as _ # noqa: F401

load_dotenv()

db_connection = os.getenv("DB_CONNECTION")
if db_connection is None:
    raise ValueError("DB_CONNECTION environment variable is not set.")

engine = create_engine(db_connection) 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as session:
        yield session

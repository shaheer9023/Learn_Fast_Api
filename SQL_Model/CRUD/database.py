from sqlmodel import SQLModel, Field, create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

# User model
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str="shaheer4414"
    password: str="4414"

# DB Config
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

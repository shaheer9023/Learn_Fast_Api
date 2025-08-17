from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Field, Session, SQLModel, create_engine, select
from jose import jwt, JWTError
from datetime import datetime, timedelta

# ========================
# Database Model
# ========================
class Myself(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

database_url = "mysql+pymysql://root:4414@127.0.0.1:3306/sql_model"
engine = create_engine(database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# ========================
# JWT Config
# ========================
SECRET_KEY = "shaheer_super_secret_key"  # apna khud ka strong key use karna
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SUPER_ADMIN = {
    "email": "shaheerahmad9023@gmail.com",
    "password": "4414"
}

# ========================
# Helper Functions
# ========================
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email != SUPER_ADMIN["email"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

# ========================
# Auth Route
# ========================
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == SUPER_ADMIN["email"] and form_data.password == SUPER_ADMIN["password"]:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# ========================
# CRUD Routes (Protected)
# ========================
@app.post("/myself/")
def create_record(record: Myself, email: str = Depends(verify_token)):
    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

@app.get("/myself/")
def read_records(email: str = Depends(verify_token)):
    with Session(engine) as session:
        records = session.exec(select(Myself)).all()
        return records

@app.put("/myself/")
def update_record(record: Myself, email: str = Depends(verify_token)):
    with Session(engine) as session:
        statement = select(Myself).where(Myself.id == record.id)
        new_record = session.exec(statement).one_or_none()
        if new_record:
            new_record.name = record.name
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            return new_record
        else:
            return {"error": "Record not found"}

@app.delete("/myself/{record_id}")
def delete_record(record_id: int, email: str = Depends(verify_token)):
    with Session(engine) as session:
        statement = select(Myself).where(Myself.id == record_id)
        record = session.exec(statement).one_or_none()
        if record:
            session.delete(record)
            session.commit()
            return {"message": "Record deleted successfully"}
        else:
            return {"error": "Record not found"}

# ========================
# Root
# ========================
@app.get("/")
def read_root():
    return {"message": "Welcome to the Myself CRUD API (JWT Protected)"}

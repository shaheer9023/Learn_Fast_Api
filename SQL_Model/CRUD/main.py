from fastapi import FastAPI
from database import create_db
from auth import router as auth_router
from crud import router as crud_router

app = FastAPI(title="Users API with JWT", version="1.0")

# DB create
create_db()

# Routers
app.include_router(auth_router)
app.include_router(crud_router)

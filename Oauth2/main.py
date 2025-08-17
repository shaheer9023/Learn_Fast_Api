from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt
app = FastAPI()

Authentication = OAuth2PasswordBearer(tokenUrl="/login")

@app.post ("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "shaheer" and form_data.password == "4414":
        token = jwt.encode({"username": form_data.username}, key="chin tapak dam dam", algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.get("/items/")
async def read_items(token: str = Depends(Authentication)):
    try:
        payload = jwt.decode(token, key="chin tapak dam dam", algorithms=["HS256"])
        return {"message": f"Hello {payload['username']}, welcome to the items page!"}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


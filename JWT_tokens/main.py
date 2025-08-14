from fastapi import FastAPI
from jose import jwt

Algo = "HS256"
secret_key = "shaheer4414"

create_jwt_token = lambda data: jwt.encode({"data":data}, secret_key, algorithm=Algo)
get_jwt_token = lambda token: jwt.decode(token, secret_key, algorithms=[Algo])

app = FastAPI()

# Ye humse data lega aur encode karke token dega
@app.get("/token")
def get_token(data)->dict:
    token = create_jwt_token(data)
    return {"token": token}

# Ye humse token lega aur decode karke data dega
@app.get("/data")
def decode_token(token: str):
    return get_jwt_token(token)

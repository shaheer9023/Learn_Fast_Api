from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(name: str | None = "shaheer", age: int = 22, limit: int = 100):
    return {"name": name, "age": age, "limit": limit}


@app.get("/items/")
async def read_items(value:Annotated[dict, Depends(common_parameters)]):
    return value["name"] # Uncomment the following lines to add another endpoint


@app.get("/users/")
async def read_users(value:Annotated[dict, Depends(common_parameters)]):
    return value
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

items = []

# --- Endpoints --- #

@app.get("/")
async def read_root():
    return {"message: " "Welcome to my API!"}

@app.get("/items/")
async def read_items():
    return items

@app.post("/items/")
async def create_items(item: Item):

    global item_id_counter
    item_id_counter += 1

    item_dict = item.dict()
    item_dict["id"] = item_id_counter
    items.append(item_dict)

    return {"message:": "Item created", "item": item_dict}

@app.get("/items/{item_id}")
async def get_item_by_id(item_id: int):

    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

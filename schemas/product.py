from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    unit_of_measure: str
    base_price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

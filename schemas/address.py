from pydantic import BaseModel
from enum import Enum

class AddressType(str, Enum):
    BILLING = 'BILLING'
    SHIPPING = 'SHIPPING'

class AddressBase(BaseModel):
    address: str
    neighborhood: str
    municipality: str
    state: str
    address_type: AddressType
    customer_id: int

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True

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

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int

    class Config:
        from_attributes = True

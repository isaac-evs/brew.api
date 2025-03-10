from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    company_name: str
    business_name: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

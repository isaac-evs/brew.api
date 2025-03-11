from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    business_name = Column(String)
    email = Column(String, unique=True, index=True)

    addresses = relationship('Address', back_populates='customer')

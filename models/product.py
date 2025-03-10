from sqlalchemy import Column, Integer, String, Float
from . import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unit_of_measure = Column(String)
    base_price = Column(Float)

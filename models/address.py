from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from . import Base

class AddressType(str, enum.Enum):
    BILLING = 'BILLING'
    SHIPPING = 'SHIPPING'

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    neighborhood = Column(String)
    municipality = Column(String)
    state = Column(String)
    address_type = Column(Enum(AddressType))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    customer = relationship('Customer', back_populates='addresses')

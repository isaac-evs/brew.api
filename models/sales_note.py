from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class SalesNote(Base):
    __tablename__ = 'sales_notes'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    billing_address_id = Column(Integer, ForeignKey('addresses.id'))
    shipping_address_id = Column(Integer, ForeignKey('addresses.id'))
    total = Column(Float)
    pdf_url = Column(String, nullable=True)

    customer = relationship('Customer')
    billing_address = relationship('Address', foreign_keys=[billing_address_id])
    shipping_address = relationship('Address', foreign_keys=[shipping_address_id])
    note_contents = relationship('SalesNoteContent', back_populates='sales_note')

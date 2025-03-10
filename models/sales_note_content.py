from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class SalesNoteContent(Base):
    __tablename__ = "sales_note_contents"

    id = Column(Integer, primary_key=True, index=True)
    sales_note_id = Column(Integer, ForeignKey("sales_notes.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    unit_price = Column(Float)
    amount = Column(Float)

    sales_note = relationship("SalesNote", back_populates="note_contents")
    product = relationship("Product")

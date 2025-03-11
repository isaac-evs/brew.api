from pydantic import BaseModel

class SalesNoteContentBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    amount: float

class SalesNoteContentCreate(SalesNoteContentBase):
    pass

class SalesNoteContent(SalesNoteContentBase):
    id: int
    sales_note_id: int

    class Config:
        from_attributes = True

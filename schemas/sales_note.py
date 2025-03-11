from pydantic import BaseModel
from typing import List, Optional
from .sales_note_content import SalesNoteContent, SalesNoteContentCreate

class SalesNoteBase(BaseModel):
    customer_id: int
    billing_address_id: int
    shipping_address_id: int
    total: float

class SalesNoteCreate(SalesNoteBase):
    note_contents: List[SalesNoteContentCreate]

class SalesNote(SalesNoteBase):
    id: int
    pdf_url: Optional[str] = None
    note_contents: List[SalesNoteContent] = []

    class Config:
        from_attributes = True

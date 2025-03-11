from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import List
from models import get_db
from schemas.sales_note import SalesNote, SalesNoteCreate
from controllers.sales_note import SalesNoteController

router = APIRouter(prefix="/sales-notes", tags=["sales-notes"])

@router.post("/", response_model=SalesNote)
def create_sales_note(sales_note: SalesNoteCreate, request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip('/')
    return SalesNoteController.create_sales_note(db=db, sales_note=sales_note, base_url=base_url)

@router.get("/{sales_note_id}", response_model=SalesNote)
def read_sales_note(sales_note_id: int, db: Session = Depends(get_db)):
    db_sales_note = SalesNoteController.get_sales_note(db, sales_note_id=sales_note_id)
    if db_sales_note is None:
        raise HTTPException(status_code=404, detail="Sales note not found")
    return db_sales_note

@router.get("/{sales_note_id}/download")
def download_sales_note(sales_note_id: int, db: Session = Depends(get_db)):
    pdf_data = SalesNoteController.get_sales_note_pdf(db, sales_note_id=sales_note_id)
    if pdf_data is None:
        raise HTTPException(status_code=404, detail="Sales note PDF not found")

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=sales_note_{sales_note_id}.pdf"
        }
    )

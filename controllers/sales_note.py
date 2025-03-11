from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from app.models.sales_note import SalesNote
from app.models.sales_note_content import SalesNoteContent
from app.models.customer import Customer
from app.models.address import Address
from app.models.product import Product
from app.schemas.sales_note import SalesNoteCreate, SalesNote as SalesNoteSchema
from app.services.pdf_service import PDFService
from app.services.aws_s3 import S3Service
from app.services.aws_ses import SESService

class SalesNoteController:
    @staticmethod
    def create_sales_note(db: Session, sales_note: SalesNoteCreate, base_url: str):
        db_sales_note = SalesNote(
            customer_id=sales_note.customer_id,
            billing_address_id=sales_note.billing_address_id,
            shipping_address_id=sales_note.shipping_address_id,
            total=sales_note.total
        )
        db.add(db_sales_note)
        db.commit()
        db.refresh(db_sales_note)

        for content_item in sales_note.note_contents:
            db_content = SalesNoteContent(
                sales_note_id=db_sales_note.id,
                **content_item.dict()
            )
            db.add(db_content)
        db.commit()
        db.refresh(db_sales_note)

        customer = db.query(Customer).filter(Customer.id == sales_note.customer_id).first()
        products = db.query(Product).all()
        addresses = db.query(Address).filter(
            (Address.id == sales_note.billing_address_id) |
            (Address.id == sales_note.shipping_address_id)
        ).all()

        pdf_data = PDFService.generate_sales_note_pdf(db_sales_note, customer, products, addresses)

        file_name = f"sales_note_{db_sales_note.id}_{uuid.uuid4()}.pdf"
        s3_service = S3Service()
        pdf_url = s3_service.upload_file(pdf_data, file_name)

        db_sales_note.pdf_url = pdf_url
        db.commit()

        download_link = f"{base_url}/sales-notes/{db_sales_note.id}/download"
        email_html = f"""
        <html>
            <body>
                <h1>Sales Note Generated</h1>
                <p>Dear {customer.company_name},</p>
                <p>Your sales note has been generated.</p>
                <p>You can download it by clicking <a href="{download_link}">here</a>.</p>
            </body>
        </html>
        """

        ses_service = SESService()
        ses_service.send_email(
            recipient=customer.email,
            subject="Sales Note Generated",
            body_html=email_html
        )

        return db_sales_note

    @staticmethod
    def get_sales_note(db: Session, sales_note_id: int):
        return db.query(SalesNote).filter(SalesNote.id == sales_note_id).first()

    @staticmethod
    def get_sales_note_pdf(db: Session, sales_note_id: int):
        sales_note = db.query(SalesNote).filter(SalesNote.id == sales_note_id).first()
        if not sales_note or not sales_note.pdf_url:
            return None

        file_name = sales_note.pdf_url.split("/")[-1]
        s3_service = S3Service()

        pdf_data = s3_service.get_file(file_name)

        s3_service.update_metadata(file_name)

        return pdf_data

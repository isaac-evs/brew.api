from operator import add
from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate, Address as AddressSchema

class AddressController:

    @staticmethod
    def get_addresses(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Address).offset(skip).limit(limit).all()

    @staticmethod
    def get_customer_addresses(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
       return db.query(Address).filter(Address.customer_id == customer_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_address(db: Session, address_id: int):
        return db.query(Address).filter(Address.id == address_id).first()


    @staticmethod
    def create_address(db: Session, address: AddressCreate):
        db_address = Address(**address.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

    @staticmethod
    def update_address(db: Session, address_id: int, address: AddressCreate):

        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address:
            for key, value in address.dict().items():
                setattr(db_address, key, value)
            db.commit()
            db.refresh(db_address)
        return db_address

    @staticmethod
    def delete_address(db: Session, address_id: int):

        db_address = db.query(Address).filter(Address.id == address_id).first()
        if db_address:
            db.delete(db_address)
            db.commit()
            return True
        return False

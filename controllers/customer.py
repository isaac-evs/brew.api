from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, Customer as CustomerSchema

class CustomerController:
    @staticmethod
    def get_customers(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Customer).offset(skip).limit(limit).all()

    @staticmethod
    def get_customer(db: Session, customer_id: int):
        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        db_customer = Customer(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    @staticmethod
    def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if db_customer:
            for key, value in customer.dict().items():
                setattr(db_customer, key, value)
            db.commit()
            db.refresh(db_customer)
        return db_customer

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if db_customer:
            db.delete(db_customer)
            db.commit()
            return True
        return False

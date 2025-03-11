from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, Product as ProductSchema

class ProductController:
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def get_product(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_product_by_name(db: Session, name: str):
        return db.query(Product).filter(Product.name == name).first()

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductCreate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            for key, value in product.dict().items():
                setattr(db_product, key, value)
            db.commit()
            db.refresh(db_product)
        return db_product

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
            return True
        return False

    @staticmethod
    def update_product_price(db: Session, product_id: int, new_price: float):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            db_product.base_price = new_price
            db.commit()
            db.refresh(db_product)
            return db_product
        return None

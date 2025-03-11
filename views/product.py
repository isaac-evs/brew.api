from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import get_db
from schemas.product import Product, ProductCreate
from controllers.product import ProductController

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = ProductController.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductController.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(
            status_code=400,
            detail=f"Product with name '{product.name}' already exists"
        )
    return ProductController.create_product(db=db, product=product)

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = ProductController.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductController.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.patch("/{product_id}/price/{new_price}", response_model=Product)
def update_product_price(product_id: int, new_price: float, db: Session = Depends(get_db)):
    if new_price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")

    db_product = ProductController.update_product_price(db, product_id=product_id, new_price=new_price)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", response_model=bool)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = ProductController.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return success

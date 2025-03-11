from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import get_db
from schemas.address import Address, AddressCreate
from controllers.address import AddressController

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/", response_model=List[Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = AddressController.get_addresses(db, skip=skip, limit=limit)
    return addresses

@router.get("/customer/{customer_id}", response_model=List[Address])
def read_customer_addresses(customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = AddressController.get_customer_addresses(db, customer_id=customer_id, skip=skip, limit=limit)
    return addresses

@router.post("/", response_model=Address)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    return AddressController.create_address(db=db, address=address)

@router.get("/{address_id}", response_model=Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = AddressController.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.put("/{address_id}", response_model=Address)
def update_address(address_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    db_address = AddressController.update_address(db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.delete("/{address_id}", response_model=bool)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    success = AddressController.delete_address(db, address_id=address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return success

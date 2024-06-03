from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db=db, request=request)

@router.get("/property/{property_id}", response_model=List[schemas.Request])
def read_requests_by_property(property_id: int, db: Session = Depends(get_db)):
    requests = crud.get_requests_by_property(db, property_id=property_id)
    return requests

@router.get("/staff/{staff_id}", response_model=List[schemas.Request])
def read_requests_by_staff(staff_id: int, db: Session = Depends(get_db)):
    requests = crud.get_requests_by_staff(db, staff_id=staff_id)
    return requests

@router.get("/guest/{guest_id}", response_model=List[schemas.Request])
def read_requests_by_guest(guest_id: int, db: Session = Depends(get_db)):
    requests = crud.get_requests_by_guest(db, guest_id=guest_id)
    return requests

@router.put("/{request_id}/assign", response_model=schemas.Request)
def update_assign_to(request_id: int, staff_id: int, db: Session = Depends(get_db)):
    db_request = crud.update_request_assign_to(db, request_id=request_id, staff_id=staff_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.put("/{request_id}/done", response_model=schemas.Request)
def update_is_done(request_id: int, is_done: bool, db: Session = Depends(get_db)):
    db_request = crud.update_request_is_done(db, request_id=request_id, is_done=is_done)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

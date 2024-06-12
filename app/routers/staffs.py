from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from ..db import crud, schemas
from ..dependencies import get_db
from ..gcs_utils import upload_to_gcs
import uuid
import os

router = APIRouter(
    prefix="/staffs",
    tags=["Staffs"],
    responses={404: {"description": "Not found"}},
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'app\serviceaccountkey.json'

BUCKET_NAME = "staff_photo_bucket"

@router.post("/", response_model=schemas.Staff)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db=db, staff=staff)

@router.put("/{staff_id}/photo", response_model=schemas.Staff)
async def update_staff_photo(staff_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    destination_blob_name = f"staff_photos/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    public_url = upload_to_gcs(file.file, BUCKET_NAME, destination_blob_name, file.content_type)
    
    db_image = crud.create_image(db=db, image=schemas.ImageCreate(filename=file.filename, url=public_url))
    db_staff = crud.update_staff_photo(db=db, staff_id=staff_id, photo_id=db_image.id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@router.delete("/{staff_id}/photo_path", response_model=schemas.Staff)
def delete_staff_photo(staff_id: int, db: Session = Depends(get_db)):
    return crud.delete_staff_photo_path(db=db, staff_id=staff_id)

@router.get("/", response_model=List[schemas.Staff])
def read_staffs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    staffs = crud.get_staffs(db, skip=skip, limit=limit)
    return staffs

@router.get("/{staff_id}", response_model=schemas.Staff)
def read_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@router.put("/{staff_id}", response_model=schemas.Staff)
def update_staff(staff_id: int, staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    db_staff = crud.update_staff(db, staff_id=staff_id, staff=staff)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@router.delete("/{staff_id}", response_model=schemas.Staff)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = crud.delete_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

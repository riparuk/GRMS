from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from ..db import crud, schemas
from ..dependencies import get_db
from ..gcs_utils import upload_to_gcs
import uuid
import os

router = APIRouter(
    prefix="/images",
    tags=["Images"],
    responses={404: {"description": "Not found"}},
)

BUCKET_NAME = "your_bucket_name"

@router.post("/", response_model=schemas.Image)
async def create_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    destination_blob_name = f"images/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    public_url = upload_to_gcs(file.file, BUCKET_NAME, destination_blob_name, file.content_type)
    
    image = schemas.ImageCreate(filename=file.filename, url=public_url)
    return crud.create_image(db=db, image=image)

@router.get("/{image_id}", response_model=schemas.Image)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.get("/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    images = crud.get_images(db, skip=skip, limit=limit)
    return images

@router.delete("/{image_id}", response_model=schemas.Image)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.delete_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

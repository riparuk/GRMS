from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db import crud, schemas
from ..gcs_utils import upload_to_gcs
from ..dependencies import get_db
import uuid
import os
import logging

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
    responses={404: {"description": "Not found"}},
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= 'app/serviceaccountkey.json'

BUCKET_NAME = "images_grms"

@router.post("/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_request(db=db, request=request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{request_id}/images", response_model=List[schemas.Image])
async def upload_request_images(request_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    images = []
    for file in files:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        destination_blob_name = f"request_images/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        public_url = upload_to_gcs(file.file, BUCKET_NAME, destination_blob_name, file.content_type)
        
        db_image = crud.create_image(db=db, image=schemas.ImageCreate(filename=file.filename, url=public_url))
        images.append(db_image)

    db_request = crud.get_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    current_image_ids = db_request.imageURLs or []
    new_image_ids = [image.id for image in images]
    current_image_ids.extend(new_image_ids)
    db_request.imageURLs = current_image_ids

    db.commit()
    db.refresh(db_request)
    
    return images

@router.get("/", response_model=List[schemas.Request])
def read_requests(
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None, 
    guest_id: Optional[int] = None,
    property_id: Optional[str] = None,
    request_id: Optional[int] = None,
    assignTo: Optional[int] = None,
    priority: Optional[float] = None,
    db: Session = Depends(get_db)
):
    requests = crud.get_requests_filtered(
        db,
        start_date=start_date,
        end_date=end_date,
        guest_id=guest_id,
        property_id=property_id,
        request_id=request_id,
        assignTo=assignTo,
        priority=priority
    )
    for request in requests:
        if request.imageURLs:
            image_details = crud.get_images_by_id(db=db, ids=request.imageURLs)
            request.imageURLs = [schemas.ImageInRequest.from_orm(image) for image in image_details]
    
    return requests

@router.put("/{request_id}/assignto/{staff_id}", response_model=schemas.Request)
def update_request_assign_to(request_id: int, staff_id: int, db: Session = Depends(get_db)):
    db_request = crud.update_request_assign_to(db=db, request_id=request_id, staff_id=staff_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request or Staff not found")
    return db_request

@router.put("/{request_id}/notes", response_model=schemas.Request)
def update_request_notes(request_id: int, notes: str, db: Session = Depends(get_db)):
    db_request = crud.update_request_notes(db=db, request_id=request_id, notes=notes)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.put("/{request_id}/update-step/{step}", response_model=schemas.Request)
def update_completion_step(request_id: int, step: int, db: Session = Depends(get_db)):
    if step not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid step")
    
    db_request, error = crud.update_request_completion_steps(db, request_id=request_id, step=step)
    if error:
        raise HTTPException(status_code=400, detail=error)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request




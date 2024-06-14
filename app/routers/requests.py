from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db import crud, schemas
from ..gcs_utils import upload_to_gcs, delete_from_gcs
from ..dependencies import get_db
import uuid
import os
import logging

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
    responses={404: {"description": "Not found"}},
)

BUCKET_NAME = "images_grms"

@router.post("/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_request(db=db, request=request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{request_id}/images", response_model=List[schemas.Image])
async def upload_request_images(request_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    db_request = crud.get_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    new_images = []
    current_image_ids = db_request.imageURLs or []
    for file in files:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        destination_blob_name = f"request_images/{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        public_url = upload_to_gcs(file.file, BUCKET_NAME, destination_blob_name, file.content_type)

        db_image = crud.create_image(db=db, image=schemas.ImageCreate(filename=file.filename, url=public_url))
        new_images.append(db_image)
        current_image_ids.append(db_image.id)

    db_request.imageURLs = current_image_ids
    db.commit()
    db.refresh(db_request)

    return [schemas.Image.from_orm(image) for image in new_images]

@router.delete("/{request_id}/images/{image_id}", response_model=schemas.Request)
def delete_request_image(request_id: int, image_id: int, db: Session = Depends(get_db)):

    # Remove reference from request
    db_request = crud.remove_image_from_request(db=db, request_id=request_id, image_id=image_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request or Image reference not found in the request")

    # Delete image from the database
    db_image = crud.delete_image(db=db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Delete image from GCS
    blob_name = "request_images/"+db_image.url.split("/")[-1]
    delete_from_gcs(BUCKET_NAME, blob_name)

    # Refresh and convert image URLs
    if db_request.imageURLs:
        image_details = crud.get_images_by_id(db=db, ids=db_request.imageURLs)
        db_request.imageURLs = [schemas.ImageInRequest.from_orm(image) for image in image_details]

    return db_request


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




from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional
from datetime import datetime
import pytz

VALID_PRIORITIES = [1.0, 2.0, 3.0, 4.0]

# Property CRUD operations
def get_property(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()

def get_properties(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Property).offset(skip).limit(limit).all()

def create_property(db: Session, property: schemas.PropertyCreate):
    db_property = models.Property(name=property.name)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, property_id: int, property: schemas.PropertyCreate):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property:
        db_property.name = property.name
        db.commit()
        db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
    return db_property

# Staff CRUD operations
def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()

def get_staffs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Staff).offset(skip).limit(limit).all()

def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(
        name=staff.name,
        property_id=staff.property_id,
        photo_path=staff.photo_path
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def update_staff_photo_path(db: Session, staff_id: int, photo_path_url: str):
    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if db_staff:
        db_staff.photo_path = photo_path_url
        db.commit()
        db.refresh(db_staff)
    return db_staff

def delete_staff_photo_path(db: Session, staff_id: int):
    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if db_staff:
        db_staff.photo_path = None
        db.commit()
        db.refresh(db_staff)
    return db_staff

def update_staff(db: Session, staff_id: int, staff: schemas.StaffCreate):
    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if db_staff:
        db_staff.name = staff.name
        db_staff.property_id = staff.property_id
        db.commit()
        db.refresh(db_staff)
    return db_staff

def delete_staff(db: Session, staff_id: int):
    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if db_staff:
        db.delete(db_staff)
        db.commit()
    return db_staff

# CRUD operations for Request
def get_request(db: Session, request_id: int):
    return db.query(models.Request).filter(models.Request.id == request_id).first()

def get_requests_by_property(db: Session, property_id: int):
    return db.query(models.Request).filter(models.Request.property_id == property_id).all()

def get_requests_by_staff(db: Session, staff_id: int):
    return db.query(models.Request).filter(models.Request.assignTo == staff_id).all()

def get_requests_by_guest(db: Session, guest_id: int):
    return db.query(models.Request).filter(models.Request.guest_id == guest_id).all()

def create_request(db: Session, request: schemas.RequestCreate):
    if request.priority not in VALID_PRIORITIES:
        raise ValueError("Invalid priority value. Valid values are: 1.0, 2.0, 3.0, 4.0.")
VALID_PRIORITIES = [1.0, 2.0, 3.0, 4.0]

def create_request(db: Session, request: schemas.RequestCreate):
    if request.priority not in VALID_PRIORITIES:
        raise ValueError("Invalid priority value. Valid values are: 1.0, 2.0, 3.0, 4.0.")
    
    tz = pytz.timezone('Asia/Jakarta')
    created_at = datetime.now(tz)
    
    db_request = models.Request(
        guest_id=request.guest_id,
        guestName=request.guestName,
        description=request.description,
        actions=request.actions,
        priority=request.priority,
        property_id=request.property_id,
        request_message="",
        assignTo=None,
        isDone=False,
        created_at=created_at,
        updated_at=created_at,
        staffName=None,
        staffImageURL=None,
        imageURLs=[],
        notes=None,
        receiveVerifyCompleted=False,
        coordinateActionCompleted=False,
        followUpResolveCompleted=False
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def update_request_assign_to(db: Session, request_id: int, staff_id: int):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request:
        db_request.assignTo = staff_id
        db_request.updated_at = datetime.now(pytz.timezone('Asia/Jakarta'))
        db.commit()
        db.refresh(db_request)
    return db_request

def update_request_completion_steps(db: Session, request_id: int, step: int):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not db_request:
        return None, "Request not found"
    
    if step == 1:
        db_request.receiveVerifyCompleted = True
    elif step == 2:
        if not db_request.receiveVerifyCompleted:
            return None, "Cannot complete coordinateActionCompleted before receiveVerifyCompleted"
        db_request.coordinateActionCompleted = True
    elif step == 3:
        if not db_request.receiveVerifyCompleted:
            return None, "Cannot complete followUpResolveCompleted before receiveVerifyCompleted"
        if not db_request.coordinateActionCompleted:
            return None, "Cannot complete followUpResolveCompleted before coordinateActionCompleted"
        db_request.followUpResolveCompleted = True
        db_request.isDone = True
    
    db_request.updated_at = datetime.now(pytz.timezone('Asia/Jakarta'))
    db.commit()
    db.refresh(db_request)
    return db_request, None



def get_requests_filtered(db: Session, startDate: datetime, endDate: datetime, guestName: Optional[str], priority: Optional[float], progress: Optional[str]):
    query = db.query(models.Request)
    
    if startDate:
        query = query.filter(models.Request.timestamp >= startDate)
    if endDate:
        query = query.filter(models.Request.timestamp <= endDate)
    if guestName:
        query = query.filter(models.Request.guestName == guestName)
    if priority:
        query = query.filter(models.Request.priority == priority)
    if progress:
        query = query.filter(models.Request.progress == progress)
    
    return query.all()



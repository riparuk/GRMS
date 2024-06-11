from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional
from datetime import datetime
import pytz

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
    db_staff = models.Staff(name=staff.name, property_id=staff.property_id)
    if staff.task_ids:
        tasks = db.query(models.Task).filter(models.Task.id.in_(staff.task_ids)).all()
        db_staff.tasks.extend(tasks)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def update_staff(db: Session, staff_id: int, staff: schemas.StaffCreate):
    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if db_staff:
        db_staff.name = staff.name
        db_staff.property_id = staff.property_id
        if staff.task_ids:
            tasks = db.query(models.Task).filter(models.Task.id.in_(staff.task_ids)).all()
            db_staff.tasks = tasks
        db.commit()
        db.refresh(db_staff)
    return db_staff

def delete_staff(db: Session, staff_id: int):
    db_staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if db_staff:
        db.delete(db_staff)
        db.commit()
    return db_staff

# Task CRUD operations
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.description = task.description
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

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
    utc_plus_7 = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(utc_plus_7)
    
    db_request = models.Request(
        guest_id=request.guest_id,
        guestName=request.guestName,
        description=request.description,
        actions=request.actions,
        priority=request.priority,
        property_id=1,  # Default value, update as necessary
        request_message="",
        assignTo=None,
        isDone=False,
        timestamp=current_time,
        progress="0/3 Done",
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
        db.commit()
        db.refresh(db_request)
    return db_request

def update_request_is_done(db: Session, request_id: int, is_done: bool):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request:
        db_request.isDone = is_done
        db.commit()
        db.refresh(db_request)
    return db_request

def get_requests_filtered(db: Session, startDate: datetime, endDate: datetime, guestName: Optional[str], priority: Optional[str], progress: Optional[str]):
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

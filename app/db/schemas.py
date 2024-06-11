# Pydantic models (schemas) that will be used when reading data, when returning it from the API.

# orm_mode = True ? 
# Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
# This way, instead of only trying to get the id value from a dict, as in:
# id = data["id"]
# it will also try to get it from an attribute, as in:
# id = data.id

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    description: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True

class StaffBase(BaseModel):
    name: str
    property_id: int

class StaffCreate(StaffBase):
    task_ids: List[int] = []

class Staff(StaffBase):
    id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True

class PropertyBase(BaseModel):
    name: str

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    staff: List[Staff] = []

    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    guest_id: int
    property_id: int
    request_message: str
    assignTo: Optional[int] = None
    isDone: bool = False

       # New attributes
    timestamp: datetime
    guestName: str
    description: str
    actions: Optional[str] = None
    priority: str
    progress: str
    staffName: Optional[str] = None
    staffImageURL: Optional[str] = None
    imageURLs: Optional[List[str]] = None
    notes: Optional[str] = None
    receiveVerifyCompleted: bool = False
    coordinateActionCompleted: bool = False
    followUpResolveCompleted: bool = False

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int

    class Config:
        orm_mode = True

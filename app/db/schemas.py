from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StaffBase(BaseModel):
    name: str
    property_id: str

class StaffCreate(StaffBase):
    photo_path: Optional[str] = None  # Ubah ini
    filename: Optional[str] = None

class Staff(StaffBase):
    id: int
    photo_path: Optional[str] = None  # Ubah ini
    filename: Optional[str] = None
    request_handled: int

    class Config:
        orm_mode = True


class PropertyBase(BaseModel):
    name: str

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: str
    staff: List[Staff] = []

    class Config:
        orm_mode = True

class RequestBase(BaseModel):
    guest_id: int
    property_id: str
    guestName: str
    description: str
    actions: Optional[str] = None
    priority: float

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    request_message: str
    assignTo: Optional[int] = None
    isDone: bool
    created_at: datetime
    updated_at: datetime
    staffName: Optional[str] = None
    staffImageURL: Optional[str] = None
    imageURLs: Optional[List[str]] = None
    notes: Optional[str] = None
    receiveVerifyCompleted: bool
    coordinateActionCompleted: bool
    followUpResolveCompleted: bool

    class Config:
        orm_mode = True
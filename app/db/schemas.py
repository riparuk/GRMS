from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ImageBase(BaseModel):
    filename: str
    url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class ImageInRequest(BaseModel):
    id: int
    filename: str
    url: str

    class Config:
        orm_mode = True
        from_attributes = True

class StaffBase(BaseModel):
    name: str
    property_id: str

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: str
    photo_path: Optional[Image] = None
    request_handled: int

    class Config:
        orm_mode = True
        from_attributes = True

class PropertyBase(BaseModel):
    name: str

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: str
    staff: List[Staff] = []

    class Config:
        orm_mode = True
        from_attributes = True

class RequestBase(BaseModel):
    guest_id: int
    property_id: str
    guestName: str
    description: str
    actions: Optional[str] = None
    priority: float = 1.0
    

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    request_message: str
    assignTo: Optional[str] = None
    isDone: bool
    created_at: datetime
    updated_at: datetime
    staffName: Optional[str] = None
    staffImageURL: Optional[Image] = None
    imageURLs: Optional[List[ImageInRequest]] = None
    notes: Optional[str] = None
    receiveVerifyCompleted: bool
    coordinateActionCompleted: bool
    followUpResolveCompleted: bool

    class Config:
        orm_mode = True
        from_attributes = True


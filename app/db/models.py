import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime, JSON, Float, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    url = Column(String, index=True)

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    property_id = Column(String, ForeignKey("properties.id"))
    photo_path = Column(JSON, nullable=True)  # Change to JSON
    request_handled = Column(Integer, default=0)
    property = relationship("Property", back_populates="staff")

class Property(Base):
    __tablename__ = "properties"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, index=True)
    staff = relationship("Staff", back_populates="property")

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, index=True)
    property_id = Column(String, index=True)
    request_message = Column(String, index=True)
    assignTo = Column(Integer, index=True, nullable=True)
    isDone = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    guestName = Column(String, index=True)
    description = Column(String, index=True)
    actions = Column(String, nullable=True)
    priority = Column(Float, index=True)
    staffName = Column(String, nullable=True)
    staffImageURL = Column(String, nullable=True)
    imageURLs = Column(JSON, nullable=True)
    notes = Column(String, nullable=True)
    receiveVerifyCompleted = Column(Boolean, default=False)
    coordinateActionCompleted = Column(Boolean, default=False)
    followUpResolveCompleted = Column(Boolean, default=False)

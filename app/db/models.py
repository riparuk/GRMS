from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

# Association table for many-to-many relationship between staff and tasks
staff_tasks = Table(
    'staff_tasks',
    Base.metadata,
    Column('staff_id', ForeignKey('staff.id'), primary_key=True),
    Column('task_id', ForeignKey('tasks.id'), primary_key=True)
)

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    staff = relationship("Staff", back_populates="property")

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))

    property = relationship("Property", back_populates="staff")
    tasks = relationship("Task", secondary=staff_tasks, back_populates="staff")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

    staff = relationship("Staff", secondary=staff_tasks, back_populates="tasks")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, index=True)
    property_id = Column(Integer, index=True)
    request_message = Column(String, index=True)
    assignTo = Column(Integer, index=True, nullable=True)
    isDone = Column(Boolean, default=False)

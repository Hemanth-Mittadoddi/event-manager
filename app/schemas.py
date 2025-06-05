from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List

class EventBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    location: constr(strip_whitespace=True, min_length=1)
    start_time: datetime
    end_time: datetime
    max_capacity: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True

class AttendeeBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr

class AttendeeCreate(AttendeeBase):
    pass

class Attendee(AttendeeBase):
    id: int
    event_id: int

    class Config:
        orm_mode = True

class AttendeeList(BaseModel):
    attendees: List[Attendee]
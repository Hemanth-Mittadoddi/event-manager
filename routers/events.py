from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.db import get_db
from datetime import datetime
import pytz

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    if event.start_time >= event.end_time:
        raise HTTPException(status_code=400, detail="start_time must be before end_time")
    db_event = crud.create_event(db, event)
    return db_event

@router.get("/", response_model=List[schemas.Event])
def list_events(db: Session = Depends(get_db)):
    return crud.get_events(db)

@router.post("/{event_id}/register", response_model=schemas.Attendee, status_code=status.HTTP_201_CREATED)
def register_attendee(event_id: int, attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if crud.get_attendee_by_email(db, event_id, attendee.email):
        raise HTTPException(status_code=400, detail="Email already registered for this event")
    attendee_count = crud.count_attendees(db, event_id)
    if attendee_count >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is fully booked")
    return crud.create_attendee(db, event_id, attendee)

@router.get("/{event_id}/attendees", response_model=schemas.AttendeeList)
def list_attendees(event_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    attendees = crud.get_attendees(db, event_id, skip, limit)
    return {"attendees": attendees}
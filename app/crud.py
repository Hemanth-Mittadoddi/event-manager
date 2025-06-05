from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session):
    return db.query(models.Event).filter(models.Event.start_time >= func.now()).order_by(models.Event.start_time).all()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_attendee_by_email(db: Session, event_id: int, email: str):
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id, models.Attendee.email == email).first()

def count_attendees(db: Session, event_id: int):
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id).count()

def create_attendee(db: Session, event_id: int, attendee: schemas.AttendeeCreate):
    db_attendee = models.Attendee(event_id=event_id, **attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

def get_attendees(db: Session, event_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id).offset(skip).limit(limit).all()
from fastapi import FastAPI
from app.db import engine, Base
from routers import events

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Event Management System")

app.include_router(events.router)
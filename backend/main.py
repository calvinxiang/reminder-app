# main.py
from fastapi import FastAPI, Depends, HTTPException
from redis import Redis
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pywebpush import webpush, WebPushException
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# VAPID keys for Web Push notifications
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize FastAPI app
app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",  # React app URL
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis setup
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# Database setup
DATABASE_URL = "postgresql://calvin:SandwichTourist16%@localhost/reminder_app"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Example DB model for reminders
class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    time = Column(DateTime)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# NEW: Pydantic model for validation
class ReminderCreate(BaseModel):
    id: int
    title: str
    time: str  # Format: 'YYYY-MM-DD HH:MM:SS'

class ReminderResponse(BaseModel):
    id: int
    title: str
    time: str

# Modify the endpoint to use the Pydantic model
@app.post("/add_reminder/")
async def add_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    # Save reminder to Redis
    reminder_id = f"reminder:{reminder.id}"
    redis_client.set(reminder_id, json.dumps(reminder.dict()))
    
    # Set expiry time for the reminder in Redis
    expiry = datetime.strptime(reminder.time, '%Y-%m-%d %H:%M:%S') - datetime.now()
    redis_client.expire(reminder_id, int(expiry.total_seconds()))
    
    # Save reminder to PostgreSQL
    db_reminder = Reminder(
        id=reminder.id,
        title=reminder.title,
        time=datetime.strptime(reminder.time, '%Y-%m-%d %H:%M:%S')
    )
    db.add(db_reminder)
    db.commit()
    
    # Send push notifications to all subscribers
    for subscription in subscriptions:
        send_push_notification(subscription, reminder.title, f"Reminder for: {reminder.time}")

    return {"status": "Reminder set!"}

# NEW: Endpoint to get all reminders
@app.get("/get_reminders/", response_model=List[ReminderResponse])
async def get_reminders(db: Session = Depends(get_db)):
    reminders = db.query(Reminder).all()
    reminders_response = [ReminderResponse(id=reminder.id, title=reminder.title, time=reminder.time.strftime('%Y-%m-%d %H:%M:%S')) for reminder in reminders]
    return reminders_response

# Web Push subscription model
class PushSubscription(BaseModel):
    endpoint: str
    keys: dict

subscriptions = []

@app.post("/subscribe/")
async def subscribe(subscription: PushSubscription):
    subscriptions.append(subscription.dict())
    return {"status": "Subscription added!"}

# Function to send push notifications
def send_push_notification(subscription, title, message):
    try:
        webpush(
            subscription_info=subscription,
            data=json.dumps({"title": title, "message": message}),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:example@example.com"},
        )
    except WebPushException as ex:
        print("Push failed: {}", repr(ex))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Event Manager

A simple FastAPI-based event management system to create and manage events and attendees with timezone support.

---

## Features

- CRUD operations for events and attendees
- Event timing stored in UTC with timezone conversions
- Prevents overbooking events (capacity limit)
- Prevents duplicate attendee registrations for the same event
- Pagination support for event and attendee lists
- Swagger UI API docs available

---

## Setup Instructions

### Prerequisites

- Python 3.9 or above
- PostgreSQL database or any supported SQL database
- Git (optional)

### Installation

1. Clone the repo or unzip the project folder:

   ```bash
   git clone <your-repo-url>
   cd event-manager
2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .venv\Scripts\activate      # Windows PowerShell
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
4. Set up environment variables:

    Create a .env file in the project root with the following content:

    ```ini
    DATABASE_URL=sqlite+aiosqlite:///./test.db
    (Modify DATABASE_URL for your preferred DB)

5. Run the app:

    ```bash
    uvicorn app.main:app --reload
6. Open http://127.0.0.1:8000/docs to access the Swagger UI API docs.

# Assumptions

- Only event organizers can update event details (name, time, location).

- Event times are input in local timezones and stored internally in UTC.

- Attendee email uniqueness is enforced per event.

- Capacity is strictly enforced to prevent overbooking.

- Simple pagination with skip and limit query params on list endpoints.

# API Usage Examples
1. Create Event

    ```bash
    curl -X POST "http://127.0.0.1:8000/events/" -H "Content-Type: application/json" -d '{
      "name": "Workshop",
      "location": "Mumbai",
      "start_time": "2025-06-10T10:00:00",
      "timezone": "Asia/Kolkata",
      "capacity": 50
    }'

2. Register Attendee

    ```bash
    curl -X POST "http://127.0.0.1:8000/events/1/attendees/" -H "Content-Type: application/json" -d '{
    "name": "Rahul Kumar",
    "email": "rahul@example.com"
    }'


3. Get Events with Pagination
    ```bash
    curl "http://127.0.0.1:8000/events/?skip=0&limit=10"
# Database Schema
The project uses SQLAlchemy models under app/models.py.

- Event model includes fields: id, name, location, start_time (UTC), timezone, capacity.

- Attendee model includes: id, name, email, event_id (ForeignKey).

The database tables are created automatically at app startup.

If you want to use Alembic for migrations, you can add it later.

# Testing
## Run tests using pytest
    ```bash
    pytest tests/test_events.py

# Notes

Make sure to install email-validator via pip install pydantic[email] as required by Pydantic.

This project uses async SQLAlchemy with sqlite+aiosqlite by default but supports other DBs with proper DATABASE_URL.


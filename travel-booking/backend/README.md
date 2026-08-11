# Travel Booking Platform – Backend

## Prerequisites

- Python 3.10+
- MySQL 8+ (create an empty database named `travel_booking`)

## Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your MySQL credentials:

```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/travel_booking
SECRET_KEY=any-long-random-string-at-least-32-characters
```

Create the database in MySQL Workbench or CLI:

```sql
CREATE DATABASE travel_booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Run

```bash
# From the backend folder
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

## Seed sample data

With the API stopped (or in another terminal with venv active):

```bash
python seed.py
```

Demo accounts:

| Role     | Email                  | Password    |
|----------|------------------------|-------------|
| Admin    | admin@travel.com       | admin123    |
| Manager  | manager@travel.com     | manager123  |
| Customer | customer@travel.com    | customer123 |

## Frontend

Open the `frontend` folder with any static server (VS Code Live Server, `npx serve`, etc.) or simply open `index.html` in a browser. CORS is enabled for local development.

Make sure the backend is running on `http://127.0.0.1:8000`.

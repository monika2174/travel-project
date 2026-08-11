# Travel Booking Platform

Full-stack travel booking application with:

- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, Bootstrap Icons
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, JWT, bcrypt
- **Database**: MySQL

## Features

- Customer registration/login, browse destinations/hotels/trips, book, cancel, favorites, reviews
- Manager: create hotels & trips, manage rooms, confirm/reject bookings
- Admin: dashboard stats, user management, approve/reject hotels & trips, delete reviews
- Role-based JWT authentication
- Responsive Bootstrap UI with Unsplash travel images

## Quick Start

### 1. Database

Create a MySQL database:

```sql
CREATE DATABASE travel_booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env → set DATABASE_URL and SECRET_KEY
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal (venv active):

```bash
python seed.py
```

### 3. Frontend

Open `frontend/index.html` with Live Server, or:

```bash
cd frontend
npx serve .
```

Then visit the URL shown (usually http://localhost:3000).

### Demo logins (after seed)

- **Admin**: admin@travel.com / admin123  
- **Manager**: manager@travel.com / manager123  
- **Customer**: customer@travel.com / customer123  

API interactive docs: http://127.0.0.1:8000/docs

## Project structure

```
travel-booking/
├── frontend/          # Static HTML/CSS/JS (Bootstrap 5)
│   ├── index.html
│   ├── login.html, register.html
│   ├── destinations.html, hotels.html, hotel-details.html
│   ├── trips.html, trip-details.html
│   ├── dashboard.html, favorites.html
│   ├── css/style.css
│   └── js/ (config, auth, api, main)
└── backend/
    ├── main.py
    ├── database.py, models.py, schemas.py, auth.py
    ├── routes/ (auth, destinations, hotels, rooms, trips, bookings, reviews, favorites, admin)
    ├── seed.py
    ├── requirements.txt
    └── .env.example
```

## Notes

- Tables are auto-created on first API start via SQLAlchemy.
- Managers’ new hotels/trips start as `pending` until an admin approves them (admin-created items are auto-approved).
- Bookings start as `pending`; managers/admins can confirm, reject, or mark completed.
- Customers can cancel only pending/confirmed bookings.
- Reviews are intended for completed bookings (enforced when booking IDs are supplied).

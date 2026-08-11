from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routes import (
    auth,
    destinations,
    hotels,
    rooms,
    trips,
    bookings,
    reviews,
    favorites,
    admin,
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Booking Platform API",
    description="Full-stack travel booking platform with hotels, trips, bookings, reviews and role-based access",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router)
app.include_router(destinations.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(trips.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(favorites.router)
app.include_router(admin.router)

# Frontend folder
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# Serve the frontend
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/health")
def health():
    return {"status": "ok"}

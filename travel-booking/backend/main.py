from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth, destinations, hotels, rooms, trips, bookings, reviews, favorites, admin

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

app.include_router(auth.router)
app.include_router(destinations.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(trips.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(favorites.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "message": "Travel Booking API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}

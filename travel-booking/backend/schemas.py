from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class UserRole(str, Enum):
    customer = "customer"
    manager = "manager"
    admin = "admin"


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    rejected = "rejected"


class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


# Auth
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.customer


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    full_name: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    role: UserRole
    is_active: bool


# Destination
class DestinationBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    starting_price: float = 0


class DestinationCreate(DestinationBase):
    pass


class DestinationOut(DestinationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool


# Hotel
class HotelCreate(BaseModel):
    name: str
    destination_id: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    star_rating: int = 3
    image_url: Optional[str] = None
    hotel_type: Optional[str] = None


class HotelUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    star_rating: Optional[int] = None
    image_url: Optional[str] = None
    hotel_type: Optional[str] = None
    is_active: Optional[bool] = None


class HotelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    location: Optional[str] = None
    description: Optional[str] = None
    star_rating: int
    image_url: Optional[str] = None
    hotel_type: Optional[str] = None
    approval_status: str
    destination_id: Optional[int] = None
    manager_id: Optional[int] = None
    is_active: bool = True


# Room
class RoomCreate(BaseModel):
    room_type: str
    price_per_night: float
    capacity: int = 2
    available_count: int = 5
    description: Optional[str] = None
    image_url: Optional[str] = None


class RoomOut(RoomCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hotel_id: int


# Trip
class TripCreate(BaseModel):
    title: str
    destination_id: Optional[int] = None
    description: Optional[str] = None
    duration_days: int
    price: float
    trip_type: Optional[str] = None
    image_url: Optional[str] = None
    included: Optional[str] = None
    excluded: Optional[str] = None


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[float] = None
    trip_type: Optional[str] = None
    image_url: Optional[str] = None
    included: Optional[str] = None
    excluded: Optional[str] = None
    is_active: Optional[bool] = None


class TripOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    duration_days: int
    price: float
    trip_type: Optional[str] = None
    image_url: Optional[str] = None
    included: Optional[str] = None
    excluded: Optional[str] = None
    approval_status: str
    destination_id: Optional[int] = None
    manager_id: Optional[int] = None
    is_active: bool = True


class ItineraryCreate(BaseModel):
    day_number: int
    title: Optional[str] = None
    description: Optional[str] = None


class ItineraryOut(ItineraryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    trip_id: int


# Bookings
class HotelBookingCreate(BaseModel):
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int = 1


class HotelBookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date
    guests: int
    nights: Optional[int] = None
    total_price: Optional[float] = None
    status: BookingStatus
    created_at: datetime
    user_id: int


class TripBookingCreate(BaseModel):
    trip_id: int
    travel_date: date
    travelers: int = 1


class TripBookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    trip_id: int
    travel_date: date
    travelers: int
    total_price: Optional[float] = None
    status: BookingStatus
    created_at: datetime
    user_id: int


class BookingStatusUpdate(BaseModel):
    status: BookingStatus


# Review
class ReviewCreate(BaseModel):
    hotel_id: Optional[int] = None
    trip_id: Optional[int] = None
    hotel_booking_id: Optional[int] = None
    trip_booking_id: Optional[int] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    description: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    hotel_id: Optional[int] = None
    trip_id: Optional[int] = None
    rating: int
    title: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime


# Favorite
class FavoriteCreate(BaseModel):
    hotel_id: Optional[int] = None
    trip_id: Optional[int] = None
    destination_id: Optional[int] = None


class FavoriteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hotel_id: Optional[int] = None
    trip_id: Optional[int] = None
    destination_id: Optional[int] = None
    created_at: datetime


# Admin dashboard
class DashboardStats(BaseModel):
    total_users: int = 0
    total_hotels: int = 0
    total_trips: int = 0
    total_bookings: int = 0
    total_revenue: float = 0
    pending_approvals: int = 0
    total_reviews: int = 0

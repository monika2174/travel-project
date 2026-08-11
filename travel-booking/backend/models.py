from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, Date,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class UserRole(str, enum.Enum):
    customer = "customer"
    manager = "manager"
    admin = "admin"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    rejected = "rejected"


class ApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    customer = relationship("Customer", back_populates="user", uselist=False)
    manager = relationship("Manager", back_populates="user", uselist=False)
    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    hotel_bookings = relationship("HotelBooking", back_populates="user")
    trip_bookings = relationship("TripBooking", back_populates="user")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    address = Column(String(255))
    user = relationship("User", back_populates="customer")


class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    company_name = Column(String(150))
    user = relationship("User", back_populates="manager")
    hotels = relationship("Hotel", back_populates="manager")
    trips = relationship("Trip", back_populates="manager")


class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    starting_price = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    hotels = relationship("Hotel", back_populates="destination")
    trips = relationship("Trip", back_populates="destination")


class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey("managers.id"), nullable=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=True)
    name = Column(String(200), nullable=False)
    location = Column(String(200))
    description = Column(Text)
    star_rating = Column(Integer, default=3)
    image_url = Column(String(500))
    hotel_type = Column(String(50))
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.pending)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    manager = relationship("Manager", back_populates="hotels")
    destination = relationship("Destination", back_populates="hotels")
    rooms = relationship("HotelRoom", back_populates="hotel", cascade="all, delete-orphan")
    amenities = relationship("HotelAmenity", back_populates="hotel", cascade="all, delete-orphan")
    bookings = relationship("HotelBooking", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")


class HotelRoom(Base):
    __tablename__ = "hotel_rooms"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"))
    room_type = Column(String(100), nullable=False)
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, default=2)
    available_count = Column(Integer, default=5)
    description = Column(Text)
    image_url = Column(String(500))

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("HotelBooking", back_populates="room")


class Amenity(Base):
    __tablename__ = "amenities"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50))


class HotelAmenity(Base):
    __tablename__ = "hotel_amenities"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"))
    amenity_id = Column(Integer, ForeignKey("amenities.id", ondelete="CASCADE"))
    hotel = relationship("Hotel", back_populates="amenities")
    amenity = relationship("Amenity")


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey("managers.id"), nullable=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    trip_type = Column(String(50))
    image_url = Column(String(500))
    included = Column(Text)
    excluded = Column(Text)
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.pending)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    manager = relationship("Manager", back_populates="trips")
    destination = relationship("Destination", back_populates="trips")
    itineraries = relationship("TripItinerary", back_populates="trip", cascade="all, delete-orphan")
    available_dates = relationship("TripDate", back_populates="trip", cascade="all, delete-orphan")
    bookings = relationship("TripBooking", back_populates="trip")
    reviews = relationship("Review", back_populates="trip")


class TripItinerary(Base):
    __tablename__ = "trip_itineraries"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"))
    day_number = Column(Integer, nullable=False)
    title = Column(String(200))
    description = Column(Text)
    trip = relationship("Trip", back_populates="itineraries")


class TripDate(Base):
    __tablename__ = "trip_dates"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"))
    available_date = Column(Date, nullable=False)
    seats_left = Column(Integer, default=20)
    trip = relationship("Trip", back_populates="available_dates")


class HotelBooking(Base):
    __tablename__ = "hotel_bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_id = Column(Integer, ForeignKey("hotel_rooms.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    guests = Column(Integer, default=1)
    nights = Column(Integer)
    total_price = Column(Float)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="hotel_bookings")
    hotel = relationship("Hotel", back_populates="bookings")
    room = relationship("HotelRoom", back_populates="bookings")


class TripBooking(Base):
    __tablename__ = "trip_bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))
    travel_date = Column(Date, nullable=False)
    travelers = Column(Integer, default=1)
    total_price = Column(Float)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="trip_bookings")
    trip = relationship("Trip", back_populates="bookings")


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=True)
    destination_id = Column(Integer, ForeignKey("destinations.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorites")
    __table_args__ = (
        UniqueConstraint("user_id", "hotel_id", name="uq_fav_hotel"),
        UniqueConstraint("user_id", "trip_id", name="uq_fav_trip"),
        UniqueConstraint("user_id", "destination_id", name="uq_fav_dest"),
    )


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    hotel_booking_id = Column(Integer, ForeignKey("hotel_bookings.id"), nullable=True)
    trip_booking_id = Column(Integer, ForeignKey("trip_bookings.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    title = Column(String(200))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")
    trip = relationship("Trip", back_populates="reviews")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    hotel_booking_id = Column(Integer, ForeignKey("hotel_bookings.id"), nullable=True)
    trip_booking_id = Column(Integer, ForeignKey("trip_bookings.id"), nullable=True)
    amount = Column(Float)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import (
    HotelBooking, TripBooking, HotelRoom, Trip, BookingStatus, User, UserRole, Manager
)
from schemas import (
    HotelBookingCreate, HotelBookingOut, TripBookingCreate, TripBookingOut, BookingStatusUpdate
)
from auth import get_current_user, require_roles

router = APIRouter(prefix="/api", tags=["Bookings"])


@router.post("/hotel-bookings", response_model=HotelBookingOut)
def create_hotel_booking(
    data: HotelBookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.check_out <= data.check_in:
        raise HTTPException(400, "Check-out must be after check-in")
    room = db.query(HotelRoom).filter(HotelRoom.id == data.room_id).first()
    if not room:
        raise HTTPException(404, "Room not found")
    nights = (data.check_out - data.check_in).days
    total = nights * room.price_per_night
    booking = HotelBooking(
        user_id=current_user.id,
        hotel_id=data.hotel_id,
        room_id=data.room_id,
        check_in=data.check_in,
        check_out=data.check_out,
        guests=data.guests,
        nights=nights,
        total_price=total,
        status=BookingStatus.pending
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/hotel-bookings", response_model=List[HotelBookingOut])
def list_hotel_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.admin:
        return db.query(HotelBooking).all()
    if current_user.role == UserRole.manager:
        manager = db.query(Manager).filter(Manager.user_id == current_user.id).first()
        if manager:
            return db.query(HotelBooking).join(HotelRoom).filter(
                HotelRoom.hotel.has(manager_id=manager.id)
            ).all()
    return db.query(HotelBooking).filter(HotelBooking.user_id == current_user.id).all()


@router.get("/hotel-bookings/{booking_id}", response_model=HotelBookingOut)
def get_hotel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(HotelBooking).filter(HotelBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role == UserRole.customer and booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    return booking


@router.put("/hotel-bookings/{booking_id}/cancel")
def cancel_hotel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(HotelBooking).filter(HotelBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role == UserRole.customer and booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    if booking.status not in [BookingStatus.pending, BookingStatus.confirmed]:
        raise HTTPException(400, "Cannot cancel this booking")
    booking.status = BookingStatus.cancelled
    db.commit()
    return {"message": "Booking cancelled"}


@router.put("/hotel-bookings/{booking_id}/status", response_model=HotelBookingOut)
def update_hotel_booking_status(
    booking_id: int,
    data: BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    booking = db.query(HotelBooking).filter(HotelBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    booking.status = data.status
    db.commit()
    db.refresh(booking)
    return booking


@router.post("/trip-bookings", response_model=TripBookingOut)
def create_trip_booking(
    data: TripBookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(Trip.id == data.trip_id).first()
    if not trip:
        raise HTTPException(404, "Trip not found")
    total = trip.price * data.travelers
    booking = TripBooking(
        user_id=current_user.id,
        trip_id=data.trip_id,
        travel_date=data.travel_date,
        travelers=data.travelers,
        total_price=total,
        status=BookingStatus.pending
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/trip-bookings", response_model=List[TripBookingOut])
def list_trip_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.admin:
        return db.query(TripBooking).all()
    if current_user.role == UserRole.manager:
        manager = db.query(Manager).filter(Manager.user_id == current_user.id).first()
        if manager:
            return db.query(TripBooking).filter(
                TripBooking.trip.has(manager_id=manager.id)
            ).all()
    return db.query(TripBooking).filter(TripBooking.user_id == current_user.id).all()


@router.get("/trip-bookings/{booking_id}", response_model=TripBookingOut)
def get_trip_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(TripBooking).filter(TripBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role == UserRole.customer and booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    return booking


@router.put("/trip-bookings/{booking_id}/cancel")
def cancel_trip_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(TripBooking).filter(TripBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if current_user.role == UserRole.customer and booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    if booking.status not in [BookingStatus.pending, BookingStatus.confirmed]:
        raise HTTPException(400, "Cannot cancel this booking")
    booking.status = BookingStatus.cancelled
    db.commit()
    return {"message": "Booking cancelled"}


@router.put("/trip-bookings/{booking_id}/status", response_model=TripBookingOut)
def update_trip_booking_status(
    booking_id: int,
    data: BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    booking = db.query(TripBooking).filter(TripBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    booking.status = data.status
    db.commit()
    db.refresh(booking)
    return booking

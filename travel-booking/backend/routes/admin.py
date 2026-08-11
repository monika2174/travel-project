from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import (
    User, Hotel, Trip, HotelBooking, TripBooking, Review,
    ApprovalStatus, BookingStatus, UserRole
)
from schemas import UserOut, HotelOut, TripOut, DashboardStats, ReviewOut
from auth import require_roles

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    total_users = db.query(User).count()
    total_hotels = db.query(Hotel).count()
    total_trips = db.query(Trip).count()
    hotel_bookings = db.query(HotelBooking).count()
    trip_bookings = db.query(TripBooking).count()
    total_bookings = hotel_bookings + trip_bookings

    hotel_rev = db.query(func.coalesce(func.sum(HotelBooking.total_price), 0)).filter(
        HotelBooking.status.in_([BookingStatus.confirmed, BookingStatus.completed])
    ).scalar() or 0
    trip_rev = db.query(func.coalesce(func.sum(TripBooking.total_price), 0)).filter(
        TripBooking.status.in_([BookingStatus.confirmed, BookingStatus.completed])
    ).scalar() or 0

    pending = (
        db.query(Hotel).filter(Hotel.approval_status == ApprovalStatus.pending).count() +
        db.query(Trip).filter(Trip.approval_status == ApprovalStatus.pending).count()
    )
    total_reviews = db.query(Review).count()

    return DashboardStats(
        total_users=total_users,
        total_hotels=total_hotels,
        total_trips=total_trips,
        total_bookings=total_bookings,
        total_revenue=float(hotel_rev) + float(trip_rev),
        pending_approvals=pending,
        total_reviews=total_reviews
    )


@router.get("/users", response_model=List[UserOut])
def list_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    if search:
        q = q.filter(
            (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )
    return q.all()


@router.put("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current_user.id:
        raise HTTPException(400, "Cannot deactivate yourself")
    user.is_active = not user.is_active
    db.commit()
    return {"message": f"User {'activated' if user.is_active else 'deactivated'}", "is_active": user.is_active}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == current_user.id:
        raise HTTPException(400, "Cannot delete yourself")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@router.get("/hotels", response_model=List[HotelOut])
def admin_list_hotels(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    q = db.query(Hotel)
    if status:
        q = q.filter(Hotel.approval_status == status)
    return q.all()


@router.put("/hotels/{hotel_id}/approve")
def approve_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    hotel.approval_status = ApprovalStatus.approved
    db.commit()
    return {"message": "Hotel approved"}


@router.put("/hotels/{hotel_id}/reject")
def reject_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    hotel.approval_status = ApprovalStatus.rejected
    db.commit()
    return {"message": "Hotel rejected"}


@router.get("/trips", response_model=List[TripOut])
def admin_list_trips(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    q = db.query(Trip)
    if status:
        q = q.filter(Trip.approval_status == status)
    return q.all()


@router.put("/trips/{trip_id}/approve")
def approve_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(404, "Trip not found")
    trip.approval_status = ApprovalStatus.approved
    db.commit()
    return {"message": "Trip approved"}


@router.put("/trips/{trip_id}/reject")
def reject_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(404, "Trip not found")
    trip.approval_status = ApprovalStatus.rejected
    db.commit()
    return {"message": "Trip rejected"}


@router.get("/reviews", response_model=List[ReviewOut])
def admin_list_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    return db.query(Review).order_by(Review.created_at.desc()).all()

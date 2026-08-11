from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Review, HotelBooking, TripBooking, BookingStatus, User, UserRole
from schemas import ReviewCreate, ReviewOut
from auth import get_current_user, require_roles

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.get("", response_model=List[ReviewOut])
def list_reviews(
    hotel_id: Optional[int] = None,
    trip_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Review)
    if hotel_id:
        q = q.filter(Review.hotel_id == hotel_id)
    if trip_id:
        q = q.filter(Review.trip_id == trip_id)
    return q.order_by(Review.created_at.desc()).all()


@router.post("", response_model=ReviewOut)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not data.hotel_id and not data.trip_id:
        raise HTTPException(400, "hotel_id or trip_id required")

    # Prevent duplicate review for same booking
    if data.hotel_booking_id:
        existing = db.query(Review).filter(Review.hotel_booking_id == data.hotel_booking_id).first()
        if existing:
            raise HTTPException(400, "Already reviewed this booking")
        booking = db.query(HotelBooking).filter(
            HotelBooking.id == data.hotel_booking_id,
            HotelBooking.user_id == current_user.id
        ).first()
        if not booking or booking.status != BookingStatus.completed:
            raise HTTPException(400, "Can only review completed bookings")

    if data.trip_booking_id:
        existing = db.query(Review).filter(Review.trip_booking_id == data.trip_booking_id).first()
        if existing:
            raise HTTPException(400, "Already reviewed this booking")
        booking = db.query(TripBooking).filter(
            TripBooking.id == data.trip_booking_id,
            TripBooking.user_id == current_user.id
        ).first()
        if not booking or booking.status != BookingStatus.completed:
            raise HTTPException(400, "Can only review completed bookings")

    review = Review(user_id=current_user.id, **data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(404, "Review not found")
    if current_user.role != UserRole.admin and review.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

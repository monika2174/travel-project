from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Trip, TripItinerary, TripDate, Manager, ApprovalStatus, User, UserRole
from schemas import TripCreate, TripOut, TripUpdate, ItineraryCreate, ItineraryOut
from auth import get_current_user, require_roles

router = APIRouter(prefix="/api/trips", tags=["Trips"])


@router.get("", response_model=List[TripOut])
def list_trips(
    destination_id: Optional[int] = None,
    trip_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Trip).filter(
        Trip.approval_status == ApprovalStatus.approved,
        Trip.is_active == True
    )
    if destination_id:
        q = q.filter(Trip.destination_id == destination_id)
    if trip_type:
        q = q.filter(Trip.trip_type.ilike(f"%{trip_type}%"))
    if min_price is not None:
        q = q.filter(Trip.price >= min_price)
    if max_price is not None:
        q = q.filter(Trip.price <= max_price)
    if search:
        q = q.filter(Trip.title.ilike(f"%{search}%"))
    return q.all()


@router.get("/{trip_id}", response_model=TripOut)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(404, "Trip not found")
    return trip


@router.post("", response_model=TripOut)
def create_trip(
    data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    manager = db.query(Manager).filter(Manager.user_id == current_user.id).first()
    trip = Trip(
        **data.model_dump(),
        manager_id=manager.id if manager else None,
        approval_status=ApprovalStatus.approved if current_user.role == UserRole.admin else ApprovalStatus.pending
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.put("/{trip_id}", response_model=TripOut)
def update_trip(
    trip_id: int,
    data: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(404, "Trip not found")
    if current_user.role == UserRole.manager:
        manager = db.query(Manager).filter(Manager.user_id == current_user.id).first()
        if not manager or trip.manager_id != manager.id:
            raise HTTPException(403, "Not your trip")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(trip, k, v)
    db.commit()
    db.refresh(trip)
    return trip


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(404, "Trip not found")
    trip.is_active = False
    db.commit()
    return {"message": "Trip deactivated"}


@router.get("/{trip_id}/itineraries", response_model=List[ItineraryOut])
def list_itineraries(trip_id: int, db: Session = Depends(get_db)):
    return db.query(TripItinerary).filter(TripItinerary.trip_id == trip_id).order_by(TripItinerary.day_number).all()


@router.post("/{trip_id}/itineraries", response_model=ItineraryOut)
def add_itinerary(
    trip_id: int,
    data: ItineraryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    item = TripItinerary(trip_id=trip_id, **data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

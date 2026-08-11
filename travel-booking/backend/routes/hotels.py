from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Hotel, HotelRoom, Manager, ApprovalStatus, User, UserRole
from schemas import HotelCreate, HotelOut, HotelUpdate, RoomCreate, RoomOut
from auth import get_current_user, require_roles

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])


@router.get("", response_model=List[HotelOut])
def list_hotels(
    location: Optional[str] = None,
    star_rating: Optional[int] = None,
    hotel_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Hotel).filter(
        Hotel.approval_status == ApprovalStatus.approved,
        Hotel.is_active == True
    )
    if location:
        q = q.filter(Hotel.location.ilike(f"%{location}%"))
    if star_rating:
        q = q.filter(Hotel.star_rating >= star_rating)
    if hotel_type:
        q = q.filter(Hotel.hotel_type.ilike(f"%{hotel_type}%"))
    if search:
        q = q.filter(Hotel.name.ilike(f"%{search}%"))
    return q.all()


@router.get("/{hotel_id}", response_model=HotelOut)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    return hotel


@router.post("", response_model=HotelOut)
def create_hotel(
    data: HotelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    manager = db.query(Manager).filter(Manager.user_id == current_user.id).first()
    hotel = Hotel(
        **data.model_dump(),
        manager_id=manager.id if manager else None,
        approval_status=ApprovalStatus.approved if current_user.role == UserRole.admin else ApprovalStatus.pending
    )
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


@router.put("/{hotel_id}", response_model=HotelOut)
def update_hotel(
    hotel_id: int,
    data: HotelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    if current_user.role == UserRole.manager:
        manager = db.query(Manager).filter(Manager.user_id == current_user.id).first()
        if not manager or hotel.manager_id != manager.id:
            raise HTTPException(403, "Not your hotel")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(hotel, k, v)
    db.commit()
    db.refresh(hotel)
    return hotel


@router.delete("/{hotel_id}")
def delete_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    hotel.is_active = False
    db.commit()
    return {"message": "Hotel deactivated"}


@router.get("/{hotel_id}/rooms", response_model=List[RoomOut])
def list_rooms(hotel_id: int, db: Session = Depends(get_db)):
    return db.query(HotelRoom).filter(HotelRoom.hotel_id == hotel_id).all()


@router.post("/{hotel_id}/rooms", response_model=RoomOut)
def add_room(
    hotel_id: int,
    data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    room = HotelRoom(hotel_id=hotel_id, **data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

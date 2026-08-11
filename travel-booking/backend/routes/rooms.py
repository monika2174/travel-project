from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import HotelRoom, Hotel, Manager, User, UserRole
from schemas import RoomCreate, RoomOut
from auth import get_current_user, require_roles

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])


@router.put("/{room_id}", response_model=RoomOut)
def update_room(
    room_id: int,
    data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    room = db.query(HotelRoom).filter(HotelRoom.id == room_id).first()
    if not room:
        raise HTTPException(404, "Room not found")
    for k, v in data.model_dump().items():
        setattr(room, k, v)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.manager, UserRole.admin))
):
    room = db.query(HotelRoom).filter(HotelRoom.id == room_id).first()
    if not room:
        raise HTTPException(404, "Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted"}

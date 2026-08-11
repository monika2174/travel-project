from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Destination, User, UserRole
from schemas import DestinationCreate, DestinationOut
from auth import get_current_user, require_roles

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])


@router.get("", response_model=List[DestinationOut])
def list_destinations(
    search: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Destination).filter(Destination.is_active == True)
    if search:
        q = q.filter(Destination.name.ilike(f"%{search}%"))
    if country:
        q = q.filter(Destination.country.ilike(f"%{country}%"))
    return q.all()


@router.get("/{destination_id}", response_model=DestinationOut)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(404, "Destination not found")
    return dest


@router.post("", response_model=DestinationOut)
def create_destination(
    data: DestinationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin, UserRole.manager))
):
    dest = Destination(**data.model_dump())
    db.add(dest)
    db.commit()
    db.refresh(dest)
    return dest


@router.put("/{destination_id}", response_model=DestinationOut)
def update_destination(
    destination_id: int,
    data: DestinationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(404, "Destination not found")
    for k, v in data.model_dump().items():
        setattr(dest, k, v)
    db.commit()
    db.refresh(dest)
    return dest


@router.delete("/{destination_id}")
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.admin))
):
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(404, "Destination not found")
    dest.is_active = False
    db.commit()
    return {"message": "Destination deactivated"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Favorite, User
from schemas import FavoriteCreate, FavoriteOut
from auth import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["Favorites"])


@router.get("", response_model=List[FavoriteOut])
def list_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Favorite).filter(Favorite.user_id == current_user.id).all()


@router.post("", response_model=FavoriteOut)
def add_favorite(
    data: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not any([data.hotel_id, data.trip_id, data.destination_id]):
        raise HTTPException(400, "Provide hotel_id, trip_id or destination_id")
    fav = Favorite(user_id=current_user.id, **data.model_dump())
    db.add(fav)
    try:
        db.commit()
        db.refresh(fav)
    except Exception:
        db.rollback()
        raise HTTPException(400, "Already in favorites or invalid reference")
    return fav


@router.delete("/{favorite_id}")
def remove_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    fav = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == current_user.id
    ).first()
    if not fav:
        raise HTTPException(404, "Favorite not found")
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favorites"}

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from models.models import Playlist, User
from dependencies import get_current_user, get_db
from schemas.schemas import PlaylistOut

router = APIRouter(prefix="/playlists", tags=["Playlists"])


@router.post("/add", response_model=PlaylistOut)
def create_playlist(
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    playlist = Playlist(name=name, user_id=current_user.id)
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


@router.put("/update/{id}", response_model=PlaylistOut)
def update_playlist(
    id: int,
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    playlist = db.query(Playlist).filter(Playlist.id == id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if playlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    playlist.name = name
    db.commit()
    db.refresh(playlist)
    return playlist


@router.delete("/delete/{id}")
def delete_playlist(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    playlist = db.query(Playlist).filter(Playlist.id == id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if playlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted"}
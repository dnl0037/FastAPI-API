from typing import Optional, List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models import User
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostVote], status_code=status.HTTP_202_ACCEPTED)
def get_posts(db: Session = Depends(get_db), user: User = Depends(oauth2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    db_posts = (db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
                .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
                .group_by(models.Post.id)
                .filter(models.Post.title.contains(search))
                .limit(limit)
                .offset(skip)
                .all())
    if not db_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return db_posts


@router.post("/", response_model=schemas.CreatedPost, status_code=status.HTTP_201_CREATED)
async def create_post(post_payload: schemas.PayloadPost, db: Session = Depends(get_db),
                      user: User = Depends(oauth2.get_current_user)):
    db_post = models.Post(**post_payload.model_dump())
    db_post.user_id = user.id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/{id_payload}", response_model=schemas.PostVote, status_code=status.HTTP_202_ACCEPTED)
async def get_post(id_payload: int, db: Session = Depends(get_db), user: User = Depends(oauth2.get_current_user)):
    # db_post = db.query(models.Post).filter(models.Post.id == id_payload).first()
    db_post = (db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
               .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
               .group_by(models.Post.id)
               .filter(models.Post.id == id_payload)
               .first())
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return db_post


@router.delete("/{id_payload}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id_payload: int, db: Session = Depends(get_db),
                      user: User = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id_payload).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to performed requested action")
    db.delete(db_post)
    db.commit()


@router.put("/{id_payload}", response_model=schemas.CreatedPost, status_code=status.HTTP_202_ACCEPTED)
async def update_post(id_payload: int, payload_post: schemas.PayloadUpdatePost, db: Session = Depends(get_db),
                      user: User = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id_payload).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if db_post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to performed requested action")
    for field, value in payload_post.model_dump(exclude_unset=True).items():
        setattr(db_post, field, value)
    db.commit()
    db.refresh(db_post)
    return db_post

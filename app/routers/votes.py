from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import utils
from .. import models, schemas, oauth2
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_200_OK)
async def vote(vote_payload: schemas.PayloadVote, db: Session = Depends(get_db),
               user: User = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == vote_payload.post_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    db_vote = db.query(models.Votes).filter(models.Votes.post_id == db_post.id, models.Votes.user_id == user.id).first()

    if vote_payload.vote_dir:
        if db_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {user.id} has already voted on post {db_post.id}")
        new_vote = models.Votes(user_id=user.id, post_id=db_post.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote successfully registered"}
    else:
        if not db_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {user.id} has not voted on post {db_post.id}")
        db.delete(db_vote)
        db.commit()
        return {"message": "Vote successfully deleted"}

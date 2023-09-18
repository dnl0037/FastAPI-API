from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import utils
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.CreatedUser, status_code=status.HTTP_201_CREATED)
async def create_user(user_payload: schemas.PayloadUser, db: Session = Depends(get_db)):
    hashed_password = utils.get_hashed(user_payload.password)
    user_payload.password = hashed_password

    db_user = models.User(**user_payload.model_dump())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@router.get("/{id_payload}", response_model=schemas.CreatedUser, status_code=status.HTTP_202_ACCEPTED)
async def get_user(id_payload: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id_payload).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return db_user

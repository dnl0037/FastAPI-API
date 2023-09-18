from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from .config import Settings as St

SECRET_KEY = St.secret_key
ALGORITHM = St.algorithm
ACCESS_TOKEN_EXPIRE = int(St.token_expiration_time)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # This gives the "not authenticated" message


def create_access_token(data: dict) -> str:
    """Returns a token with the user ID along with the Secret key, algorithm and expiration time"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """Decodes token and extracts the ID of the user. """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        decoded_payload_id = decoded_payload.get("user_id", None)

        if not decoded_payload_id:
            raise credentials_exception
        token_data = schemas.TokenData(id=decoded_payload_id, )
    except JWTError:
        raise credentials_exception
    else:
        return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extracts the id from the decoded token"""
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    verified_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == verified_token.id).first()
    if not user:
        raise credentials_exception
    return user

# User wants to make a post -> post function has a dependency (get_current_user) -> This dependency redirects the call
# to the verify function -> this decodes the token, checks if there is an ID and returns it. If there is not an
# ID, raises an error.
# qué pasa si el usuario no existe? Se verifica en get_current_user

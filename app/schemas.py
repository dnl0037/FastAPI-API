from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

"""RECEIVE FROM CLIENT"""


class PayloadPost(BaseModel):
    title: str  # Si no tiene "=", el valor es obligatorio
    content: str
    published: Optional[bool] = True


class PayloadUser(BaseModel):
    email: EmailStr
    password: str


class PayloadUpdatePost(PayloadPost):
    published: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PayloadVote(BaseModel):
    post_id: int
    vote_dir: conint(ge=0, le=1)


"""GIVE TO CLIENT"""


class CreatedUser(BaseModel):
    id: int
    email: str
    created_at: datetime


class PostUser(BaseModel):
    id: int
    email: str


class CreatedPost(PayloadPost):
    id: int
    created_at: datetime
    user_id: int
    user: PostUser


class PostComplete(BaseModel):
    Post: CreatedPost
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


"""INTERNAL"""


class TokenData(BaseModel):
    id: Optional[int] = None

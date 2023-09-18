from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, login, votes
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) -> Creates db tables. No needed if using alembic.
app = FastAPI()
origins = [
    "https://www.google.com",
    "http://localhost:8080",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"David": "MEEEEEEEEEEEEEEEEEE"}

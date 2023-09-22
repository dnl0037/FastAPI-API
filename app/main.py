from fastapi import FastAPI, Request
from .routers import posts, users, login, votes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# models.Base.metadata.create_all(bind=engine) -> Creates db tables. No needed if using alembic.
app = FastAPI()
origins = [
    "*",
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

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    message = "Ese David, mi causa, ¡bótame tu me!"
    image_url = request.url_for('static', path='cuy.jpg')
    return templates.TemplateResponse("index.html", {"request": request, "message": message, "image_url": image_url})

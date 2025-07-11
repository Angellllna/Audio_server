from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.track import router as track_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from db.database import Base, engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(track_router)

templates = Jinja2Templates(directory="templates")


# Головна сторінка
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    from db.database import SessionLocal
    from models.models import Track
    db = SessionLocal()
    tracks = db.query(Track).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "tracks": tracks})

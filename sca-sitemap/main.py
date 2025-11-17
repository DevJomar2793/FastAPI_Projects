from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from routers import auth, dashboard
from database import Base, engine
from models import User


app = FastAPI() # Initialize FastAPI app

#Create Tables
Base.metadata.create_all(bind=engine)

#Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.state.templates = templates

#Routers
app.include_router(auth.router)
app.include_router(dashboard.router)

    

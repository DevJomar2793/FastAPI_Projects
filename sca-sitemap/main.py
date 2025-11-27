from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from Backend.routers import auth, dashboard, buyer
from Backend.database import Base, engine



app = FastAPI() # Initialize FastAPI app
app.add_middleware(SessionMiddleware, secret_key="1234555") # Session Middleware

#Create Tables
Base.metadata.create_all(bind=engine)

#Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="Frontend/templates/login")
# app.state.templates = templates

#Routers
app.include_router(auth.router)
app.include_router(dashboard.router)  # Dashboard router
app.include_router(buyer.router)      # Buyer router

    

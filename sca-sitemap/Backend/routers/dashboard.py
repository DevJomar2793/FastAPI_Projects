from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from Backend.dependency import get_current_user



router = APIRouter(prefix="/dashboard") # Define router
templates = Jinja2Templates(directory="Frontend/templates")

# Dashboard Page
@router.get("/")
def dashboard(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})
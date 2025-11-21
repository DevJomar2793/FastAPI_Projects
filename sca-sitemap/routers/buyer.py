from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dependency import get_current_user




router = APIRouter(prefix="/buyer") # Define router
templates = Jinja2Templates(directory="templates") 

# Dashboard Page
@router.get("/", name="buyer_dashboard")
def dashboard(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse("buyer.html", {"request": request, "user": current_user})



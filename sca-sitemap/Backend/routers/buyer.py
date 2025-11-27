from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Backend.dependency import get_current_user
from Backend.database import get_db
from Backend.models import BuyerPage


router = APIRouter(prefix="/buyer") # Define router
templates = Jinja2Templates(directory="Frontend/templates") 

# User Profile
@router.get("/", name="buyer_dashboard")
def dashboard(request: Request, success: int | None = None, current_user = Depends(get_current_user)):
    return templates.TemplateResponse("buyer.html", {"request": request, "user": current_user, "success": success})



@router.post("/add-page")
def add_buyer_page(request: Request,
                   alpha: str = Form(...),
                   screen_number: int = Form(...),
                   screen_type: str = Form(...),
                   screen_description: str = Form(...),
                   file_label: str = Form(...),
                   screen_label: str = Form(...),
                   notes: str = Form(...),
                   sitemap: str = Form(...),
                   db: Session = Depends(get_db)):
    
    new_page = BuyerPage(
        alpha=alpha,
        screen_number=screen_number,
        screen_type=screen_type,
        screen_description=screen_description,
        file_label=file_label,
        screen_label=screen_label,
        notes=notes,
        sitemap=sitemap
    )

    db.add(new_page)
    db.commit()

    print({"message": "Added Successfully"})
    return RedirectResponse("/buyer?success=1", status_code=302)
    



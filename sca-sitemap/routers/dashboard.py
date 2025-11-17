from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter() 

# Dashboard Page
@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    
    #Get user_id from cookies
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/login")
    
    #Query user from DB
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return RedirectResponse("/login")
    
    #Render dashboard with user info
    return request.app.state.templates.TemplateResponse("dashboard.html", {"request": request, "user_name": user.full_name})
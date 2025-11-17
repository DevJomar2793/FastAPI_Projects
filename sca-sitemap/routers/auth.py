from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import User
from passlib.context import CryptContext
  
router = APIRouter() # Define router
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password hashing context
 

# Login Page
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login/login.html", {"request": request})

# Login Action
@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    # Query user from DB
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse("/login?error=invalid", status_code=303)
    
    if not pwd_context.verify(password, user.password):
        return RedirectResponse("/login?error=invalid", status_code=303)
    
    # Set cookie and redirect to dashboard
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id))
    return response

# Register Page                           
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return request.app.state.templates.TemplateResponse("login/signup.html", {"request": request})

# Register Action
@router.post("/register")
def register(request: Request, full_name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    
    # hash password
    hashed_pw = pwd_context.hash(password)

    # Create new user
    new_user = User(full_name=full_name, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse("/login?success=1", status_code=302)
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User
from passlib.context import CryptContext
  
router = APIRouter() # Define router
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password hashing context


# Landing Page
@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return request.app.state.templates.TemplateResponse("index.html", {"request": request})


# Forgot-Password Page
@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page(request: Request):
    return request.app.state.templates.TemplateResponse("forgot-password.html", {"request": request})
 

# Login Page
@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login.html", {"request": request})

# Login Action
@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    # Query user from DB
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse("/login?error=invalid", status_code=303)
    
    if not pwd_context.verify(password, user.password):
        return RedirectResponse("/login?error=invalid", status_code=303)
    
    # Store user info in session
    request.session["user_id"] = user.id
    return RedirectResponse("/dashboard", status_code=302)

# Register Page                           
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return request.app.state.templates.TemplateResponse("signup.html", {"request": request})

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

@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("user_id")
    return response

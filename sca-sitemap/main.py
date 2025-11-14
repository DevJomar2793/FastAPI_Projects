from fastapi import FastAPI, HTTPException, Request, Form, Depends # Import FastAPI and necessary modules
from fastapi.responses import HTMLResponse, RedirectResponse # Import response classes
from fastapi.templating import Jinja2Templates # Import Jinaja2 Templates
from fastapi.staticfiles import StaticFiles # Import Static Files handling
from starlette.middleware.sessions import SessionMiddleware # Import Session Middleware
from sqlalchemy.orm import Session # Import SQLAlchemy Session
from passlib.context import CryptContext # Import Passlib for password hashing
from database import Base, engine, SessionLocal # Import databae setup
from models import User # Import User model
from schemas import UserCreate, UserResponse # Import Pydantic Schemas


# Base.metadata.drop_all(bind=engine) # Use this line only if you want to drop existing tables
Base.metadata.create_all(bind=engine) # Create tables based on models

app = FastAPI() # Initiative FastAPI app
templates = Jinja2Templates(directory="templates") # Set templates Directory

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password Hashing Context

#Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Render Home Page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Render Login Page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

@app.post("/login")
def login(request: Request, email:str = Form(...), password: str = Form(...)):
    if email == ["email"] and password == ["password"]:
        request.session["email"] = email # Store email in session
        return RedirectResponse(url="/", status_code=303)
    else:
        return templates.TemplateResponse("login/login.html", {"request": request, "error": "Invalid Credentials"})
    

# Render signup page
@app.get("/signup", name="signup", response_class=HTMLResponse)
def open_register_page(request: Request):
    return templates.TemplateResponse("login/signup.html", {"request": request})

#Handle form submission for user registration
@app.post("/create-user", response_class=HTMLResponse)
def register_user(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    ):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.full_name == full_name, User.email == email).first()
        if existing_user:
            return templates.TemplateResponse("login/signup.html",
                {"request": request, "error": "User with this email already exists."},
                )
        
        # Hash the password
        hashed_password = pwd_context.hash(password)
        new_user = User(full_name=full_name, email=email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Redirect to Login Page after Successful Registration
        return templates.TemplateResponse(
            "login/login.html",
            {"request": request, "Success": "Account created successfully. Please login."},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Render Forgot Password Page
@app.get("/forgot-password", name="forgot-password", response_class=HTMLResponse)
def forgot_password(request: Request):
    return templates.TemplateResponse("login/forgot-password.html", {"request": request})


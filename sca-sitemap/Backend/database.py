from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configure your database URL here
DATABASE_URL = "mysql+pymysql://root:1234555@localhost:8889/sca-sitemap-v2"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

#Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
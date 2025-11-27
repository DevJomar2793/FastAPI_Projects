from sqlalchemy import Column, Integer, String
from Backend.database import Base

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

# Buyer Page model
class BuyerPage(Base):
    __tablename__ = "buyer_page"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    alpha = Column(String(10), nullable=False)
    screen_number = Column(Integer, nullable=False)
    screen_type = Column(String(50), nullable=False)
    screen_description = Column(String(255), nullable=False)
    file_label = Column(String(100), nullable=False)
    screen_label = Column(String(100), unique=True, nullable=False)
    notes = Column(String(255), nullable=False)
    sitemap = Column(String(255), nullable=False)


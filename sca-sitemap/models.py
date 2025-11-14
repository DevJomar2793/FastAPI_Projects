from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
   


class ScreenList(Base):
    __tablename__ = "screen_list"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    screen_number = Column(Integer, unique=True, index=True, nullable=False)
    screen_type = Column(String(50), nullable=False)
    
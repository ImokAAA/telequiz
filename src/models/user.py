from datetime import datetime as dt
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
  
class User(Base):
    __tablename__ = 'users'

    telegram_id = mapped_column(Integer, unique=True, nullable=False)
    name = mapped_column(String(128), unique=True, nullable=True)
    email = mapped_column(String(128), unique=True, nullable=True)
    phone = mapped_column(String(16), unique=True, nullable=True)
    role = mapped_column(String(16), default='user')

    quizes = relationship("Quiz", back_populates="owner")
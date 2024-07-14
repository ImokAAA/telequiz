from datetime import datetime as dt
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Quiz(Base):
    __tablename__ = 'quizes'
   
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
 
    owner = relationship("User", back_populates="quizes")
    questions = relationship("Question", back_populates="quiz")

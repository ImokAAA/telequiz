from datetime import datetime as dt
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Question(Base):
    __tablename__ = 'questions'

    name = mapped_column(String(128), unique=True, nullable=False)
    quiz_id = mapped_column(Integer, ForeignKey("quizes.id"))
    

    answers = relationship("Answer", back_populates="question")
    quiz = relationship("Quiz", back_populates="questions")
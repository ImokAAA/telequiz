from datetime import datetime as dt
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Answer(Base):
    __tablename__ = 'answers'

    name = mapped_column(String(128), unique=True, nullable=False)
    question_id = mapped_column(Integer, ForeignKey("questions.id"))
    correct_answer = mapped_column(Boolean, nullable=True)

    question = relationship("Question", back_populates="answers")
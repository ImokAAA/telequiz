from datetime import datetime as dt
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User_answer(Base):
    __tablename__ = 'user_answers'

    user_id = mapped_column(Integer, ForeignKey("users.id"))
    question_id = mapped_column(Integer, ForeignKey("questions.id"))
    answer_id = mapped_column(Integer, ForeignKey("answers.id"))
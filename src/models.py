from datetime import datetime as dt
from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=dt.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)


class User(BaseModel):
    __tablename__ = 'users'

    telegram_id: Mapped[str] = mapped_column(Integer, unique=True, nullable=False)
    name = mapped_column(String(128), unique=True, nullable=True)
    email = mapped_column(String(128), unique=True, nullable=True)
    phone = mapped_column(String(16), unique=True)
    role = mapped_column(String(16), default='user')

    quizes = relationship("Quiz", back_populates="owner")

class Quiz(BaseModel):
    __tablename__ = 'quizes'

    name = mapped_column(String(128), unique=True, nullable=False)
    owner_id = mapped_column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="quizes")
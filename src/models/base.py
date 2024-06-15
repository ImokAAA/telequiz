from typing import Annotated
from datetime import datetime as dt
 
from fastapi import Depends

from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import settings

class Base(DeclarativeBase):
    __abstract__ = True
  
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=dt.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)


engine = create_async_engine(
    settings.DB_URL,
    echo=True
)
SessionLocal = sessionmaker(autocommit=False,class_= AsyncSession, autoflush=False, bind=engine)



async def get_db():
    async with SessionLocal() as session:
        yield session


db_dependency = Annotated[SessionLocal, Depends(get_db)]
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    async_scoped_session, 
    AsyncSession
)  
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the parent directory of src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.config import settings

'''
class DatabaseHelper:
    def __init__(self, url:str, echo:bool=False  ):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False
        )     
    def get_scope_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        ) 
        return session
    
    async def session_dependency(self) -> AsyncSession:
        async with self.get_scope_session() as sess:
            yield sess
              

db_helper = DatabaseHelper(
    url=settings.DB_URL,
    echo=settings.DB_ECHO
)
'''
# Create the async engine and sessionmaker
engine = create_async_engine(settings.DB_URL, echo=settings.DB_ECHO)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
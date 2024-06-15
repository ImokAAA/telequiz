from models.base import SessionLocal
from models import User, Quiz, Answer
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
'''
def save_user_to_db(telegram_id: int):
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        new_user = User(telegram_id = telegram_id)
        session.add(new_user)
        session.commit()
    session.close()
'''
async def save_user_to_db(session:AsyncSession, telegram_id: int):
    print(type(telegram_id))
    stmt_user = select(User).where(User.telegram_id == telegram_id)
    result1: Result = await session.execute(stmt_user)
    user = result1.scalars().first()
    if not user:
        new_user = User(telegram_id = telegram_id)
        session.add(new_user)
        await session.commit()
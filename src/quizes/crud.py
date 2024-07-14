from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import SessionLocal
from models import User, Quiz, Answer

async def save_quiz_to_db(session: AsyncSession, telegram_id: int, quiz_name:str):
    stmt_user = select(User).where(User.telegram_id == telegram_id)
    result1: Result = await session.execute(stmt_user)
    user = result1.scalars().first()
    stmt_quiz = select(Quiz).where(Quiz.owner_id == user.id, Quiz.name == quiz_name)
    result2: Result = await session.execute(stmt_quiz)
    quiz = result2.scalars().first()
    if not quiz:
        new_quiz = Quiz(owner_id = user.id, name = quiz_name)
        session.add(new_quiz)
        await session.commit()

async def get_user_quizes_name(session: AsyncSession, telegram_id: int):
    stmt_user = select(User).where(User.telegram_id == telegram_id)
    result1: Result = await session.execute(stmt_user)
    user = result1.scalars().first()
    stmt = select(Quiz).where(Quiz.owner_id==user.id).order_by(Quiz.id)
    result:Result = await session.execute(stmt)
    quizes = result.scalars().all()
    quizes_names_only = [str(quiz.name) for quiz in quizes]
    return quizes_names_only

async def get_quiz_by_name(session: AsyncSession, name: str):
    stmt = select(Quiz).where(Quiz.name==name).order_by(Quiz.id)
    result:Result = await session.execute(stmt)
    quiz = result.scalars().first()
    return quiz
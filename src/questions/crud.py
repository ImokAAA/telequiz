from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import SessionLocal
from models import Quiz, Quiz, Question

async def save_question_to_db(session: AsyncSession, quiz_name:str, question_name):
    stmt_quiz = select(Quiz).where(Quiz.name == quiz_name)
    result1: Result = await session.execute(stmt_quiz)
    quiz = result1.scalars().first()
    stmt_question = select(Question).where(Question.quiz_id == quiz.id, Question.name == question_name)
    result2: Result = await session.execute(stmt_question)
    question = result2.scalars().first()
    if not question:
        new_question = Question(quiz_id = quiz.id, name = question_name)
        session.add(new_question)
        await session.commit()

async def get_quiz_questions(session: AsyncSession, quiz_name:str):
    stmt_quiz = select(Quiz).where(Quiz.name == quiz_name)
    result1: Result = await session.execute(stmt_quiz)
    quiz = result1.scalars().first()
    stmt = select(Question).where(Question.quiz_id==quiz.id).order_by(Question.id)
    result:Result = await session.execute(stmt)
    questions = result.scalars().all()
    return questions

async def get_question_by_id(session: AsyncSession, id: int):
    stmt = select(Question).where(Question.id==id).order_by(Question.id)
    result:Result = await session.execute(stmt)
    question = result.scalars().first()
    return question
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import SessionLocal
from models import Quiz, Quiz, Question, Answer

async def save_answer_to_db(session: AsyncSession, question_id:int, answer_name:str, is_correct:bool):
    stmt_answer = select(Answer).where(Answer.question_id == question_id, Answer.name == answer_name)
    result2: Result = await session.execute(stmt_answer)
    answer = result2.scalars().first()
    if not answer:
        new_answer = Answer(question_id = question_id, name = answer_name, correct_answer = is_correct)
        session.add(new_answer)
        await session.commit()

async def get_question_answers_name(session: AsyncSession, question_id:int):
    stmt = select(Answer).where(Answer.question_id==question_id).order_by(Answer.id)
    result:Result = await session.execute(stmt)
    answers = result.scalars().all()
    answers_names_only = [str(answer.name) for answer in answers]
    return answers_names_only

async def get_answer_by_id(session: AsyncSession, id: int):
    stmt = select(Answer).where(Answer.id==id).order_by(Answer.id)
    result:Result = await session.execute(stmt)
    answer = result.scalars().first()
    return answer
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import SessionLocal
from models import Quiz, Quiz, Question, Answer

async def get_question_by_quiz_name_and_index(session: AsyncSession, quiz_name: str, index:int):
    stmt_quiz = select(Quiz).where(Quiz.name == quiz_name)
    result1: Result = await session.execute(stmt_quiz)
    quiz = result1.scalars().first()
    stmt = select(Question).where(Question.quiz_id==quiz.id).order_by(Question.id)
    result:Result = await session.execute(stmt)
    questions = result.scalars().all()
    if(index+1 > len(questions)): return None
    else: return questions[index]

async def get_answers_by_question_id(session: AsyncSession, question_id: int):
    stmt = select(Answer).where(Answer.question_id==question_id).order_by(Answer.created_at)
    result:Result = await session.execute(stmt)
    answers = result.scalars().all()
    return answers

async def check_if_answer_correct_by_id(session: AsyncSession, answer_id: int) -> bool:
    stmt = select(Answer).where(Answer.id==answer_id).order_by(Answer.created_at)
    result:Result = await session.execute(stmt)
    answer = result.scalars().first()
    if(answer.correct_answer): return True
    else: return False
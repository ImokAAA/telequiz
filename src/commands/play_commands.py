from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from aiogram import types

from models import get_db
from src.questions.crud import save_question_to_db
from src.quizes.crud import get_quiz_by_name, get_user_quizes_name
from src.answers.crud import get_answer_by_id
from src.play.crud import get_question_by_quiz_name_and_index, check_if_answer_correct_by_id, get_answers_by_question_id
import keyboards as kb
router = Router()

class Play(StatesGroup):
     quiz_name = State()
     question_index = State()
     score = State()
     current_question = State()

@router.callback_query(F.data == "play")
async def clb_start_play(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    async for sess in get_db():
        quizes = await get_user_quizes_name(session=sess, telegram_id=telegram_id)
    await callback.message.edit_text('Выбери квиз', 
                         reply_markup= await kb.inline_quizes_play(quiz_names=quizes))


@router.callback_query(F.data.startswith("quiz_play_"))
async def clb_quiz_play(callback: CallbackQuery, state = FSMContext):
    quiz_name = callback.data.split('_')[2]
    async for sess in get_db():
        quiz = await get_quiz_by_name(session=sess, name=quiz_name)
        question = await get_question_by_quiz_name_and_index(session=sess,\
                                                              quiz_name=quiz_name, index=0)
        answers = await get_answers_by_question_id(session= sess, question_id=question.id)
    await state.update_data(quiz_name = quiz_name)
    await state.update_data(question_index = 0)
    await state.update_data(current_question = question.name)
    await callback.message.edit_text(text=f"Playing the quiz: {quiz.name}\
                                    \n1. {question.name}", reply_markup=await kb.inline_quizes_play_question(answers=answers))

@router.callback_query(F.data.startswith("answer_check_"))
async def clb_check_play(callback: CallbackQuery, state = FSMContext):
    answer_id = callback.data.split('_')[2]
    question_id = callback.data.split('_')[3]
    data = await state.get_data()
    print("Question index " + str(data["question_index"]))
    print("Cur question" + str(data["current_question"]))
    await state.update_data(question_index = data["question_index"] + 1)
    async for sess in get_db():
        is_correct = await check_if_answer_correct_by_id(session=sess, answer_id=answer_id)
        answers = await get_answers_by_question_id(session= sess, question_id=question_id)
    if(is_correct): res = "Correct"
    else: res = "Incorrect"
    await callback.message.edit_text(text=f"{res} answer: {data['quiz_name']}\
                                    \n1. {data['current_question']}", reply_markup=await kb.inline_quizes_play_question_result(answers=answers, answer_id=answer_id, question_id=question_id))


@router.callback_query(F.data.startswith("answer_play_"))
async def clb_next_play(callback: CallbackQuery, state = FSMContext):
    data = await state.get_data()
    async for sess in get_db():
        question = await get_question_by_quiz_name_and_index(session=sess,\
                                                              quiz_name=data['quiz_name'], index=data['question_index'])
    if question:
        await state.update_data(current_question = question.name)
        async for sess in get_db():
            answers = await get_answers_by_question_id(session= sess, question_id=question.id)
        await callback.message.edit_text(text=f"Playing the quiz: {data['quiz_name']}\
                                    \n1. {question.name}", reply_markup=await kb.inline_quizes_play_question(answers=answers))

    else:
        await callback.message.edit_text(text=f"End the quiz: {data['quiz_name']}",\
                                          reply_markup=kb.main)

    
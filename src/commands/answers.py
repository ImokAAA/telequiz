from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models import get_db
from src.answers.crud import save_answer_to_db
from answers.crud import get_answer_by_id
import keyboards as kb
router = Router()

class Answer(StatesGroup):
     question_id = State()
     name = State()
     quiz_name = State()
     is_correct = State()

@router.callback_query(F.data.startswith("answers_"))
async def clb_list_answers(callback: CallbackQuery):
    question_id = callback.data.split("_")[1]
    quiz_name = callback.data.split("_")[2]
    await callback.message.edit_text('Список ответов', 
                         reply_markup= await kb.inline_answers(question_id=question_id, quiz_name=quiz_name))

@router.callback_query(F.data.startswith("answer_add_"))
async def cmd_create_answer(callback: CallbackQuery, state: FSMContext):
    question_id = callback.data.split("_")[2]
    quiz_name = callback.data.split("_")[3]
    await state.update_data(question_id = question_id)
    await state.update_data(quiz_name = quiz_name)
    await state.set_state(Answer.name)
    await callback.bot.send_message(text='Введите имя для вашего ответа:', chat_id=callback.from_user.id)

@router.message(Answer.name)
async def answer_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Answer.is_correct)
    await message.answer(text='Введите +/- чтобы отметить правильность вашего ответа:')

@router.message(Answer.is_correct)
async def answer_correct(message: Message, state: FSMContext):
    is_correct = False
    if(message.text == "+"):
        is_correct = True
    await state.update_data(is_correct = str(is_correct))
    data = await state.get_data()
    async for sess in get_db():
        await save_answer_to_db(session = sess, question_id = data['question_id'], answer_name = data['name'], is_correct = is_correct)
    await message.answer(f"Ваш ответ {data['name']} был создан", 
                         reply_markup= await kb.inline_answers(question_id=data['question_id'], quiz_name=data['quiz_name']))
    await state.clear()

@router.callback_query(F.data.startswith("answer_correct_"))
async def cmd_correct_answer(callback: CallbackQuery):
    question_id = callback.data.split("_")[2]
    quiz_name = callback.data.split("_")[3]
    
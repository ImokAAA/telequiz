from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models import get_db
from src.questions.crud import save_question_to_db
from quizes.crud import get_quiz_by_name
import keyboards as kb
router = Router()

class Question(StatesGroup):
     quiz_name = State()
     name = State()

@router.callback_query(F.data.startswith("questions_"))
async def clb_list_questions(callback: CallbackQuery):
    await callback.message.edit_text('Список вопросов', 
                         reply_markup= await kb.inline_questions(callback.data[len('questions_'):]))

@router.callback_query(F.data.startswith("question_add_"))
async def cmd_create_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(quiz_name = callback.data[len('question_add_'):])
    await state.set_state(Question.name)
    await callback.bot.send_message(text='Введите имя для вашего вопроса:', chat_id=callback.from_user.id)

@router.message(Question.name)
async def question_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    async for sess in get_db():
        await save_question_to_db(session = sess, quiz_name = data['quiz_name'], question_name = data['name'])
    await message.answer(f"Ваш вопрос {data['name']} был создан", 
                         reply_markup= await kb.inline_questions(quiz_name=data['quiz_name']))
    await state.clear()

@router.callback_query(F.data.startswith("question_info_"))
async def clbk(callback: CallbackQuery):
    question_id = callback.data.split('_')[2]
    quiz_name = callback.data.split('_')[3]
    await callback.message.edit_text(f"{quiz_name}", 
                         reply_markup= await kb.inline_question_menu(question_id = question_id, quiz_name=quiz_name)
                        )
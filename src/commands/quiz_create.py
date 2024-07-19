from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models import get_db
from quizes.crud import save_quiz_to_db

router = Router()

class Quiz(StatesGroup):
     name = State()

@router.message(Command('create_quiz'))
async def cmd_create_quiz(message: Message, state: FSMContext):
    await state.set_state(Quiz.name)
    await message.answer('Введите имя для вашего квиза:')

@router.message(Quiz.name)
async def quiz_name(message: Message, state: FSMContext,  session:AsyncSession = Depends(get_db)):
    await state.update_data(name = message.text)
    data = await state.get_data()
    async for sess in get_db():
        await save_quiz_to_db(session = sess, telegram_id = message.chat.id, quiz_name= data['name'])
    await message.answer(f"Ваш квиз {data['name']} был создан")
    await state.clear()


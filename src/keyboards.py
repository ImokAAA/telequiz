from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.quizes.crud import get_user_quizes_name

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

#from models import db_helper
from models import get_db

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои квизы', callback_data='quizes')],
    [InlineKeyboardButton(text='Мои данные', callback_data='personal')]
    ]
)

async def inline_quizes(telegram_id:int):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        quizes = await get_user_quizes_name(session=sess, telegram_id=telegram_id)
    for quiz in quizes:
        keyboard.add(InlineKeyboardButton(text=quiz, \
                                          url='https://www.youtube.com/watch?v=qRyshRUA0xM&list=PLV0FNhq3XMOJ31X9eBWLIZJ4OVjBwb-KM&index=4')
                     )
    return keyboard.adjust(2).as_markup()

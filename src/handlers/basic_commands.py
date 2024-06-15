from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from models import get_db
from src.users.crud import save_user_to_db
import keyboards as kb
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    async for sess in get_db():
        await save_user_to_db(session = sess, telegram_id=message.chat.id)
    await message.answer('Привет. \nЭтот бот может организовать квизы для совместной игры в групповых чатах. Также вы можете создавать собственные квизы. \nНапиши команду /create_quiz для создания квизов.')

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Contact the admin of the bot: @zhumangali_imangali')

@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer('Главное меню', 
                         reply_markup= kb.main)
    
@router.callback_query(F.data == 'quizes')
async def clbk(callback: CallbackQuery):
    await callback.message.edit_text('Список квизов', 
                         reply_markup= await kb.inline_quizes(callback.message.chat.id)
                        )
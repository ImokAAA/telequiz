import logging

import aiogram
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

 
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет. \nЭтот бот может организовать квизы для совместной игры в групповых чатах. Также вы можете создавать собственные квизы. \nНапиши команду /create_quiz для создания квизов.')

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('/help')


'''
@dp.business_message()
async def echo_message(message: Message):
    await message.answer('Сьебался')
'''

@dp.message(Command('create_quiz'))
async def create_quiz(message: Message):
    await message.answer('Quiz created')

async def main():
    await dp.start_polling(bot)

if   __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #REMOVE IN PROD
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print("Bye bye...")
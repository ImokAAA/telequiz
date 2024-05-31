import uvicorn
import logging
import aiogram
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Update
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .config import settings
from .services import save_user_to_db
from .models import BaseModel
from .routers import (
    user,
    tg
)

nrock_ip = "https://imangali.space"
WEBHOOK_URL = f"{nrock_ip}/webhook"

BaseModel.metadata.create_all(bind=engine)
bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    save_user_to_db(message.from_user.id)
    await message.answer('Привет. \nЭтот бот может организовать квизы для совместной игры в групповых чатах. Также вы можете создавать собственные квизы. \nНапиши команду /create_quiz для создания квизов.')

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('help')

app = FastAPI()
#app.include_router(user.router)

'''
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    save_user_to_db(message.from_user.id)
    await message.reply("Hello World")

'''

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = Update.model_validate(await request.json(), context={'bot':bot}) 
        #Dispatcher.set_current(dp)
        #Bot.set_current(bot)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Error processing update")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

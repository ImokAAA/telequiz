import uvicorn
import logging
import aiogram
import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Update
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.base import engine
from config import settings
from src.models import Base, db_helper
from handlers import routers_list

nrock_ip = "https://bdd3-77-245-106-179.ngrok-free.app"
WEBHOOK_URL = f"{nrock_ip}/webhook"

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEBHOOK_URL) 
    for router in routers_list:
        dp.include_router(router)
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await bot.delete_webhook()
app = FastAPI(lifespan=lifespan)
#app.include_router(user.router)

'''
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    save_user_to_db(message.from_user.id)
    await message.reply("Hello World")

'''

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

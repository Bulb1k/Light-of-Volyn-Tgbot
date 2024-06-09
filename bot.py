from data.config import BOT_TOKEN
from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

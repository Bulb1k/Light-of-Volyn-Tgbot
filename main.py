from aiogram import Dispatcher
import asyncio
import sys
from bot import bot
from data import redis
from heandlers.notifications import send_notification_off_light

import heandlers


async def main():
    print("Configuring aiogram")
    dp = Dispatcher(storage=redis.redis_storage)

    dp.include_router(heandlers.prepare_router())

    await bot.delete_webhook(drop_pending_updates=True)
    print("Configured aiogram")
    asyncio.create_task(send_notification_off_light())

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

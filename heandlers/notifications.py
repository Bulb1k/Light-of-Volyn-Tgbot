from bot import bot
from services.database import DB
from datetime import datetime, timedelta
import pytz
import asyncio


async def time_left_light(hours: str):
    timezone = pytz.timezone('Europe/Kiev')

    hours_start = datetime.strptime(hours.split('-')[0], '%H:%M').time()
    hours_start = datetime.combine(datetime.today(), hours_start)
    hours_start = timezone.localize(hours_start)

    now_utc = datetime.now(pytz.utc)
    now = now_utc.astimezone(timezone)

    notification_time = hours_start - timedelta(minutes=30)
    time_left = (hours_start - now).seconds // 60
    return time_left


async def send_notification_off_light():
    notified_times = {}

    while True:
        list_chat_id = await DB.select_all("""SELECT chat_id FROM users""")
        if not list_chat_id:
            continue

        current_date = datetime.now(pytz.timezone('Europe/Kiev')).date()

        for chat_id in list_chat_id:
            schedule = await DB.select_one("""SELECT schedule FROM users WHERE chat_id = ?""", chat_id)
            if not schedule:
                continue
            list_hours = schedule[0].split(', ')
            for hours in list_hours:
                time_left = await time_left_light(hours)
                last_notified_time = notified_times.get(chat_id)
                if time_left <= 30 and f'{current_date} {hours}' != last_notified_time:
                    await bot.send_message(*chat_id, f"Вимкнення світла станеться через {time_left}хв. 🕯")
                    notified_times[*chat_id] = f'{current_date} {hours}'

        await asyncio.sleep(15 * 60)



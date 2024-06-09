from aiogram import types
from aiogram.fsm.context import FSMContext
from heandlers.state import StartState
from scraper.parser import get_schedule
from services.database import DB


async def greeting(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer('Привіт, я бот який допоможе тобі дізнатись твій графік виклюення світла ⚡️')
    await message.answer('Введіть ваш нас. пункт 🌇')

    await state.set_state(StartState.waiting_settlement)


async def search_settlement(message: types.Message, state: FSMContext):
    await message.answer('Зачекайте, ведеться пошук 🔎')
    settlement = message.text

    list_schedule = await get_schedule(settlement)

    if list_schedule is None or len(list_schedule) == 0:
        await message.answer('Вибачте вашого нас. пукнту немає у списку 🚫')
        await message.answer('Можливо ви вказали невірний нас. пукнт або для вашого нас. пункту немає графіку!')
        return

    await message.answer('Введіть назву вашої вулиці 🌇')
    await state.update_data(ListSchedule=list_schedule, Settlement=settlement)
    await state.set_state(StartState.waiting_street)


async def search_street(message: types.Message, state: FSMContext):
    street = message.text
    data = await state.get_data()
    list_schedule = data.get('ListSchedule')
    settlement = data.get('Settlement')

    temporary_list_schedule = []
    for schedule in list_schedule:
        if schedule['settlement'] == settlement:
            if schedule['street'] == street:
                temporary_list_schedule.append(schedule)

    if len(temporary_list_schedule) == 0:
        await message.answer('Вибачте вашого нас. пукнту немає у списку 🚫')
        await message.answer('Можливо ви вказали невірну вулицю або для вашої вулиці немає графіку!')
        return

    await message.answer('Введіть номер будинку 🏡')
    await state.update_data(ListSchedule=temporary_list_schedule, Street=street)
    await state.set_state(StartState.waiting_house)


async def search_house(message: types.Message, state: FSMContext):
    house = message.text
    data = await state.get_data()
    list_schedule = data.get('ListSchedule')
    settlement = data.get('Settlement')
    street = data.get('Street')

    for schedule in list_schedule:
        if house in schedule['houses']:
            await state.update_data(Schedule=schedule, House=house)
            await output_schedule(message, state)
            return

    await message.answer('Вибачте вашого вулиці немає у списку 🚫')
    await message.answer('Можливо ви вказали невірну вулицю або для вашої вулиці немає графіку!')
    return


async def output_schedule(message: types.Message, state: FSMContext):
    data = await state.get_data()
    schedule = data.get('Schedule')
    chat_id = message.chat.id

    await message.answer(f'{schedule["date"]} 📅'
                         f'\n{schedule["settlement"]}, вул. {schedule["street"]} {data.get("House")}'
                         f'\n{schedule["hours"]} ⏰')

    await DB.insert("""INSERT INTO users (chat_id, settlement, street, house, notifications_enabled, schedule)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                    (chat_id, data.get('Settlement'), data.get('Street'), data.get('House'), True, schedule['hours']))


async def cabinet_menu(message: types.Message, state: FSMContext):
    pass

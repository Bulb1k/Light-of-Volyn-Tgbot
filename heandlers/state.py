from aiogram.fsm.state import State, StatesGroup


class StartState(StatesGroup):
    waiting_settlement = State()
    waiting_street = State()
    waiting_house = State()


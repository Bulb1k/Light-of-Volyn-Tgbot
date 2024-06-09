from aiogram.filters import CommandStart
from aiogram import Router, F
from heandlers import register_address
from heandlers.state import StartState


def prepare_router() -> Router:
    router = Router()

    router.message.register(register_address.greeting, CommandStart())
    router.message.register(register_address.search_settlement, StartState.waiting_settlement)
    router.message.register(register_address.search_street, StartState.waiting_street)
    router.message.register(register_address.search_house, StartState.waiting_house)

    return router

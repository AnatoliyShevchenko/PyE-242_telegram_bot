# Aiogram
from aiogram.fsm.state import State, StatesGroup


class ExchangeStates(StatesGroup):
    currency_request = State()
    wait_sum = State()

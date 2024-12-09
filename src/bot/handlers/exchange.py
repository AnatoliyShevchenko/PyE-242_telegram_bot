# Python
import json

# Aiogram
from aiogram import Router
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

# Third-Party
import aiofiles

# Local
from src.bot.states import ExchangeStates
from src.settings.base import VOLUME


exchange_router = Router()


@exchange_router.callback_query(ExchangeStates.action_request)
async def select_currency(callback: CallbackQuery, state: FSMContext):
    action = callback.data
    await state.update_data(data={"action": action})
    rub = InlineKeyboardButton(text="RUB", callback_data="RUB")
    usd = InlineKeyboardButton(text="USD", callback_data="USD")
    kzt = InlineKeyboardButton(text="KZT", callback_data="KZT")
    markup = InlineKeyboardMarkup(inline_keyboard=[[rub], [usd], [kzt]])
    await state.set_state(state=ExchangeStates.currency_request)
    await callback.message.answer(
        text="Выберите валюту", reply_markup=markup
    )


@exchange_router.callback_query(ExchangeStates.currency_request)
async def currency_request(callback: CallbackQuery, state: FSMContext):
    async with aiofiles.open(
        file=VOLUME + f"{callback.data}.json", mode="r"
    ) as f:
        temp = await f.read()
        data = json.loads(temp)
    await state.update_data(data={"data": data})
    await state.set_state(state=ExchangeStates.wait_sum)
    await callback.message.answer(
        text="Сколько валюты вы хотите купить/продать?"
    )



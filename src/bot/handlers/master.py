# Aiogram
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


master_router = Router()


@master_router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text="Здравствуйте, это мой тестовый бот")


@master_router.message(Command("exchange"))
async def select_currency(message: Message):
    rub = InlineKeyboardButton(text="RUB", callback_data="RUB")
    usd = InlineKeyboardButton(text="USD", callback_data="USD")
    kzt = InlineKeyboardButton(text="KZT", callback_data="KZT")
    markup = InlineKeyboardMarkup(inline_keyboard=[[rub], [usd], [kzt]])
    await message.answer(text="Выберите валюту", reply_markup=markup)

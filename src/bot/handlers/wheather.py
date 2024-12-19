# Aiogram
from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext

# Local
from src.bot.states import WheatherStates
from src.bot.utils.wheather import get_current_wheather


wheather_router = Router()


@wheather_router.callback_query(
    WheatherStates.current_or_forecast, F.data == "current"
)
async def request_for_city_current(
    callback: CallbackQuery, state: FSMContext
):
    await state.update_data(data={"status": callback.data})
    await state.set_state(state=WheatherStates.request_for_city)
    await callback.message.answer(text="Введите название города")


@wheather_router.callback_query(
    WheatherStates.current_or_forecast, F.data == "forecast"
)
async def request_for_city_forecast(
    callback: CallbackQuery, state: FSMContext
):
    await callback.message.answer(text="Функция пока не реализована")


@wheather_router.message(WheatherStates.request_for_city)
async def wait_city_current(message: Message, state: FSMContext):
    data = await state.get_data()
    status = data.get("status")
    if status == "forecast":
        return
    current_wheather: dict = await get_current_wheather(
        city_name=message.text
    )
    if not current_wheather:
        await message.answer(
            text="Что-то пошло не так, введите название города корректно!"
        )
    else:
        temp = current_wheather["temp_c"]
        condition = current_wheather["condition"]["text"]
        wind = current_wheather["wind_kph"]
        humidity = current_wheather["humidity"]
        template = f"""Температура воздуха {temp}, кондиция {condition},
        ветер {wind} км/ч, влажность воздуха {humidity}."""
        await state.clear()
        await message.answer(text=template)

# Third-Party
from aiohttp import ClientSession

# Local
from src.settings.base import WHEATHER_KEY, logger


BASE_URL = "http://api.weatherapi.com/v1"
CURRENT = "/current.json"
FORECAST = "/forecast.json"


async def get_current_wheather(city_name: str):
    url = (f"{BASE_URL}{CURRENT}?key={WHEATHER_KEY}" 
        f"&q={city_name}&aqi=no")
    async with ClientSession() as session:
        try:
            response = await session.get(url=url)
            response.raise_for_status()
        except Exception as e:
            logger.error(
                "Something went wrong while during "
                f"function {__name__}: {e}"
            )
            return None
        data: dict[dict] = await response.json()
    current = data.get("current")
    return current


async def get_wheather_forecast(city_name: str, days_count: int = 0):
    url = (
        f"{BASE_URL}{FORECAST}?key={WHEATHER_KEY}"
        f"&q={city_name}&days={days_count}&aqi=no&alerts=no"
    )

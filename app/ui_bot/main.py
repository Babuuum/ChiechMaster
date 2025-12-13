from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.ui_bot.handlers.start import router as start_router
from app.ui_bot.handlers.league import router as chiech_master_router

from app.config import get_settings

settings = get_settings()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(chiech_master_router)
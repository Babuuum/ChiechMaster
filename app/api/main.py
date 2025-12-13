from fastapi import FastAPI
from .routers.user import router as user_router
from app.ui_bot.main import dp, bot
from app.config import get_settings


app = FastAPI(title='Chiech_Master')

app.include_router(user_router)


@app.on_event("startup")
async def on_startup():
    await dp.start_polling(bot)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

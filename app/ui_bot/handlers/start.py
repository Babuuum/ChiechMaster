from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from app.core.db.session import async_session
from app.core.services.user import UserService

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_tg_id = message.from_user.id
    username = message.from_user.username or f"user_{user_tg_id}"

    # Создаем сессию через async_session (это async_sessionmaker)
    session = async_session()

    try:
        # Начинаем транзакцию
        async with session.begin():
            user = await UserService.get_or_create_user(
                session,
                tg_id=user_tg_id,
                tg_nickname=username
            )

            await message.answer(
                f"Привет, {username}!\n"
                f"Статус: {'Активен' if user.is_active else 'Неактивен'}"
            )
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
        raise
    finally:
        await session.close()
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.core.db.session import async_session
from app.core.services.league_db_services import LeagueServices
from app.ui_bot.messages.league import format_chiech_master_message

router = Router()


@router.message(Command('chiech_master'))
async def cmd_chiech_master(message: Message):
    session = async_session()

    try:
        async with session.begin():
            # Получаем лигу
            league = await LeagueServices.get_actual_leagues(session)

            if not league:
                await message.answer("Активная лига не найдена.")
                return

            # Получаем цели и большие цели для лиги
            # В зависимости от вашей реализации сервисов, вам может понадобиться:
            # 1. Либо цели уже загружены в league.goals и league.big_goals
            # 2. Либо нужно загрузить их отдельно

            # Пример, если нужно загрузить отдельно:
            # league_goals = await LeagueServices.get_league_goals(session, league.id)
            # league_big_goals = await LeagueServices.get_league_big_goals(session, league.id)

            # Если цели уже в объекте league:
            league_goals = league.goals
            league_big_goals = league.big_goals

            # Форматируем сообщение
            formatted_message = format_chiech_master_message(
                league,
                league_goals,
                league_big_goals
            )

            # Отправляем сообщение
            await message.answer(
                formatted_message,
                parse_mode="HTML"  # Используем HTML вместо Markdown для цветов
            )

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
        raise
    finally:
        await session.close()
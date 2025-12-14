from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.core.db.session import async_session
from app.core.services.league_db_services import LeagueServices
from app.ui_bot.messages.league import format_chiech_master_message

router = Router()


@router.message(Command('chiech_master'))
async def cmd_chiech_master(message: Message):

    leagues_list = LeagueServices

    for league in leagues_list:
        if not league:
            await message.answer("Активная лига не найдена.")


        formatted_message = format_chiech_master_message(
            league.league_name,
            league.legue_goals,
            league.league_big_goals
        )

        await message.answer(
            formatted_message,
            parse_mode="HTML"
        )


#sdelat' toje samoe dl9 usera
#potestit' s real'nimi dannimi
#sdelat' refactoring

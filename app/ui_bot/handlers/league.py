from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from app.core.services.league_db_services import LeagueServices
from app.ui_bot.messages.league import format_league_message_markdown

router = Router()


@router.message(Command('chiech_master'))
async def cmd_chiech_master(message: Message):
    try:
        leagues_list = await LeagueServices.get_actual_leagues()

        if not leagues_list:
            await message.answer("Активные лиги не найдены.")
            return

        for league in leagues_list:
            formatted_message = format_league_message_markdown(
                league,
                league.goals,
                league.big_goals,
            )

            # Если сообщение слишком длинное, разбиваем его
            if len(formatted_message) > 4000:
                # Разбиваем сообщение на части
                parts = []
                current_part = []
                current_length = 0

                for line in formatted_message.split('\n'):
                    line_length = len(line)
                    if current_length + line_length + 1 > 4000:  # +1 для символа новой строки
                        parts.append('\n'.join(current_part))
                        current_part = [line]
                        current_length = line_length
                    else:
                        current_part.append(line)
                        current_length += line_length + 1

                if current_part:
                    parts.append('\n'.join(current_part))

                # Отправляем части по очереди
                for i, part in enumerate(parts):
                    await message.answer(
                        part,
                        parse_mode="Markdown"
                    )
            else:
                await message.answer(
                    formatted_message,
                    parse_mode="Markdown"
                )

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
from dataclasses import dataclass
from typing import List

from sqlalchemy import select

from app.core.db.session import async_session
from app.core.db.models.chiech_master import League


class LeagueServices:
    @staticmethod
    async def get_actual_leagues() -> list:
        try:
            async with async_session as session:
                leagues = await session.execute(select(League).where(League.active==True))

                leagues_list = []

                for league in leagues:
                    league_name = league.name
                    league_goals = league.goals
                    league_big_goals = league.big_goals

                    leagues_list.append(
                        LeagueServicesDC(
                        league_name,
                        league_goals,
                        league_big_goals,
                    ))

        except Exception as e:
            print(f'Ошибка базы данных: {e}')
            raise
        finally:
            await session.close()

        return leagues_list



@dataclass
class LeagueServicesDC:

    league_name: League | None
    league_goals: List | None
    league_big_goals: List | None



from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.core.db.session import async_session
from app.core.db.models.chiech_master import League


@dataclass
class GoalDC:
    id: int
    name: str
    big_goal_id: int
    description: Optional[str]
    usual: Optional[bool]
    completed: bool
    difficult: str  # или GoalsDifficult если импортировать enum


@dataclass
class BigGoalDC:
    id: int
    name: str
    description: Optional[str]
    completed: bool
    goals: List[GoalDC]


@dataclass
class LeagueServicesDC:
    id: int
    name: str
    active: bool
    ended: bool
    start_league_date: datetime
    format: str  # или LeagueFormat если импортировать enum
    goals: List[GoalDC]
    big_goals: List[BigGoalDC]


class LeagueServices:
    @staticmethod
    async def get_actual_leagues() -> List[LeagueServicesDC]:
        try:
            async with async_session() as session:  # Исправлено: async_session()
                # Загружаем лиги с их целями и большими целями
                stmt = (
                    select(League)
                    .where(League.active == True)
                    .options(
                        selectinload(League.goals),  # Загружаем все goals
                        selectinload(League.big_goals)  # Загружаем все big_goals
                    )
                )

                result = await session.execute(stmt)
                leagues = result.scalars().all()

                leagues_list = []

                for league in leagues:
                    # Преобразуем goals в GoalDC
                    goals_dc = []
                    for goal in league.goals:
                        goals_dc.append(GoalDC(
                            id=goal.id,
                            name=goal.name,
                            big_goal_id=goal.big_goal_id,
                            description=goal.description,
                            usual=goal.usual,
                            completed=goal.completed,
                            difficult=goal.difficult.value if hasattr(goal.difficult, 'value') else str(goal.difficult)
                        ))

                    # Преобразуем big_goals в BigGoalDC
                    big_goals_dc = []
                    for big_goal in league.big_goals:
                        # Получаем цели для каждой большой цели
                        big_goal_goals = []
                        for goal in big_goal.goals:
                            big_goal_goals.append(GoalDC(
                                id=goal.id,
                                name=goal.name,
                                big_goal_id=goal.big_goal_id,
                                description=goal.description,
                                usual=goal.usual,
                                completed=goal.completed,
                                difficult=goal.difficult.value if hasattr(goal.difficult, 'value') else str(
                                    goal.difficult)
                            ))

                        big_goals_dc.append(BigGoalDC(
                            id=big_goal.id,
                            name=big_goal.name,
                            description=big_goal.description,
                            completed=big_goal.completed,
                            goals=big_goal_goals
                        ))

                    # Создаем объект LeagueServicesDC
                    leagues_list.append(LeagueServicesDC(
                        id=league.id,
                        name=league.name,
                        active=league.active,
                        ended=league.ended,
                        start_league_date=league.start_league_date,
                        format=league.format.value if hasattr(league.format, 'value') else str(league.format),
                        goals=goals_dc,
                        big_goals=big_goals_dc
                    ))

                return leagues_list

        except Exception as e:
            print(f'Ошибка базы данных: {e}')
            raise



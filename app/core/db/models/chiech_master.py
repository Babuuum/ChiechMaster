from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, TEXT, BOOLEAN, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as SQLEnum

from app.core.db.base import Base
from .enums import LeagueFormat, GoalsDifficult


class League(Base):
    __tablename__ = 'league'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    start_league_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    format: Mapped[LeagueFormat] = mapped_column(
        SQLEnum(LeagueFormat),
        default=LeagueFormat.NORMAL,
        nullable=False
    )

    goals: Mapped[List['Goals']] = relationship(
        secondary="league_goals",
        back_populates='league'
    )
    big_goals: Mapped[List['BigGoals']] = relationship(
        secondary="league_big_goals",
        back_populates='league'
    )


class BigGoals(Base):
    __tablename__ = 'big_goals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    goals: Mapped[List["Goals"]] = relationship(back_populates='big_goals')

    user: Mapped[List['User']] = relationship(
        secondary="user_big_goals",
        back_populates='big_goals'
    )
    league: Mapped[List[League]] = relationship(
        secondary="league_big_goals",
        back_populates='big_goals'
    )


class Goals(Base):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    big_goal_id: Mapped[int] = mapped_column(ForeignKey("big_goals.id"))
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    usual: Mapped[Optional[bool]] = mapped_column(BOOLEAN, nullable=True)

    big_goals: Mapped['BigGoals'] = relationship(back_populates='goals')

    user: Mapped[List['User']] = relationship(
        secondary="user_goals",
        back_populates='goals'
    )
    league: Mapped[List[League]] = relationship(
        secondary="league_goals",
        back_populates='goals'
    )

    difficult: Mapped[GoalsDifficult] = mapped_column(
        SQLEnum(GoalsDifficult),
        default=GoalsDifficult.NORMAL,
        nullable=False
    )
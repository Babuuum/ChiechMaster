from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, TEXT, BOOLEAN, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum as SQLEnum

from app.core.db.base import Base
from .enums import MedsDayTime


class BadHabits(Base):
    __tablename__ = 'bad_habits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    in_progress: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    completed: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    user: Mapped['User'] = relationship(back_populates='bad_habits')
    bad_habit_stats: Mapped[List['BadHabitStats']] = relationship(back_populates='bad_habit')


class BadHabitStats(Base):
    __tablename__ = 'bad_habit_stats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    daily_report: Mapped[str] = mapped_column(String, nullable=False)
    bad_habit_id: Mapped[int] = mapped_column(ForeignKey('bad_habits.id'))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    bad_habit: Mapped["BadHabits"] = relationship(back_populates='bad_habit_stats')


class Meds(Base):
    __tablename__ = 'meds'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    dose: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    daytime: Mapped[Optional[MedsDayTime]] = mapped_column(
        SQLEnum(MedsDayTime),
        nullable=True
    )

    user: Mapped["User"] = relationship(back_populates='meds')


class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates='tasks')

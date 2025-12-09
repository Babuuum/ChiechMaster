from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, ForeignKey, DateTime, String, TEXT, Enum as SQLEnum, BOOLEAN, Table, Column
from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import Optional, List

from app.core.db.base import Base

user_goals = Table(
    "user_goals",
    Base.metadata,
    Column("user_id", ForeignKey('user.id'), primary_key=True),
    Column('goals_id', ForeignKey('goals.id'), primary_key=True)
)

user_big_goals = Table(
    "user_big_goals",
    Base.metadata,
    Column("user_id", ForeignKey('user.id'), primary_key=True),
    Column('big_goals_id', ForeignKey('big_goals.id'), primary_key=True)
)

user_roadmaps = Table(
    "user_roadmaps",
    Base.metadata,
    Column("user_id", ForeignKey('user.id'), primary_key=True),
    Column('roadmap_id', ForeignKey('roadmap.id'), primary_key=True)
)

league_goals = Table(
    "league_goals",
    Base.metadata,
    Column('league_id', ForeignKey('league.id'), primary_key=True),
    Column('goals_id', ForeignKey('goals.id'), primary_key=True)
)

league_big_goals = Table(
    "league_big_goals",
    Base.metadata,
    Column('league_id', ForeignKey('league.id'), primary_key=True),
    Column('big_goals_id', ForeignKey('big_goals.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tg_nickname: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    notes: Mapped[List["Notes"]] = relationship(back_populates='user')
    information: Mapped[List["Information"]] = relationship(back_populates='user')
    bad_habits: Mapped[List["BadHabits"]] = relationship(back_populates='user')
    meds: Mapped[List["Meds"]] = relationship(back_populates='user')
    tasks: Mapped[List["Tasks"]] = relationship(back_populates='user')

    goals: Mapped[List['Goals']] = relationship(
        secondary=user_goals,
        back_populates='user'
    )
    big_goals: Mapped[List['BigGoals']] = relationship(
        secondary=user_big_goals,
        back_populates='user'
    )
    roadmaps: Mapped[List['Roadmap']] = relationship(
        secondary=user_roadmaps,
        back_populates='user'
    )


class LeagueFormat(Enum):
    CHILL = 'chill' #duration 2 weeks
    SOFT = 'soft' #duration 1 month
    NORMAL = 'normal' #duration 3 month

class GoalsDifficult(Enum):
    VERY_EASY = 'very_easy'
    EASY = 'easy'
    NORMAL = 'normal'
    HARD = 'hard'
    INSANE = 'insane'


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
        secondary=league_goals,
        back_populates='league'
    )
    big_goals: Mapped[List['BigGoals']] = relationship(
        secondary=league_big_goals,
        back_populates='league'
    )


class BigGoals(Base):
    __tablename__ = 'big_goals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    goals: Mapped[List["Goals"]] = relationship(back_populates='big_goals')

    user: Mapped[List['User']] = relationship(
        secondary=user_big_goals,
        back_populates='big_goals'
    )
    league: Mapped[List[League]] = relationship(
        secondary=league_big_goals,
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
        secondary=user_goals,
        back_populates='goals'
    )
    league: Mapped[List[League]] = relationship(
        secondary=league_goals,
        back_populates='goals'
    )

    difficult: Mapped[GoalsDifficult] = mapped_column(
        SQLEnum(GoalsDifficult),
        default=GoalsDifficult.NORMAL,
        nullable=False
    )


class Notes(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates='notes')


class Information(Base):
    __tablename__ = 'information'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    href: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates='information')


class Roadmap(Base):
    __tablename__ = 'roadmap'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    custom: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    classes: Mapped[List["Classes"]] = relationship(back_populates='roadmap')

    user: Mapped[List['User']] = relationship(
        secondary=user_roadmaps,
        back_populates='roadmaps'
    )


class Classes(Base):
    __tablename__ = 'classes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    roadmap_id: Mapped[int] = mapped_column(ForeignKey('roadmap.id'))
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    roadmap: Mapped["Roadmap"] = relationship(back_populates='classes')


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


class MedsDayTime(Enum):
    BEFORE_BREAKFAST = 'BEFORE_BREAKFAST'
    BREAKFAST = 'BREAKFAST'
    AFTER_BREAKFAST = 'AFTER_BREAKFAST'
    BEFORE_LUNCH = 'BEFORE_LUNCH'
    LUNCH = 'LUNCH'
    AFTER_LUNCH = 'AFTER_LUNCH'
    DINNER = "DINNER"
    BEFORE_DINNER = "BEFORE_DINNER"
    AFTER_DINNER = "AFTER_DINNER"


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

    user: Mapped["USER"] = relationship(back_populates='tasks')

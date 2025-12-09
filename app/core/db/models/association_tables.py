from sqlalchemy import Table, Column, ForeignKey
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
from datetime import datetime, timezone
from typing import List
from sqlalchemy import Integer, String, DateTime, BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.core.db.base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tg_nickname: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)

    notes: Mapped[List["Notes"]] = relationship(back_populates='user')
    information: Mapped[List["Information"]] = relationship(back_populates='user')
    bad_habits: Mapped[List["BadHabits"]] = relationship(back_populates='user')
    meds: Mapped[List["Meds"]] = relationship(back_populates='user')
    tasks: Mapped[List["Tasks"]] = relationship(back_populates='user')

    # Импорты для отношений Many-to-Many (будут определены позже)
    goals: Mapped[List['Goals']] = relationship(
        secondary="user_goals",
        back_populates='user'
    )
    big_goals: Mapped[List['BigGoals']] = relationship(
        secondary="user_big_goals",
        back_populates='user'
    )
    roadmaps: Mapped[List['Roadmap']] = relationship(
        secondary="user_roadmaps",
        back_populates='user'
    )

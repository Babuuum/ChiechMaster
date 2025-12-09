from typing import Optional, List
from sqlalchemy import Integer, String, BOOLEAN, ForeignKey, TEXT
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.core.db.base import Base


class Roadmap(Base):
    __tablename__ = 'roadmap'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    custom: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    classes: Mapped[List["Classes"]] = relationship(back_populates='roadmap')

    user: Mapped[List['User']] = relationship(
        secondary="user_roadmaps",
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


class Notes(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
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
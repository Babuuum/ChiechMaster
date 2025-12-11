from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.core.db.models import User
from app.core.db.session import SessionDep

router = APIRouter(tags=['/user'])


class UserBase(BaseModel):
    tg_id: int = Field(..., gt=0)
    tg_nickname: str = Field(..., min_length=1, max_length=50)
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    tg_id: int = Field(..., gt=0)
    tg_nickname: str = Field(..., min_length=1, max_length=50)


@router.get('/users')
async def get_user_list(session: SessionDep):
    stmt = select(User)
    user_list = session.scalars(stmt)
    return {'users' : user_list}

@router.post('/users/create')
async def create_user(session: SessionDep, user_data=UserCreate):
    existing = await session.execute(select(User).where(User.tg_id == user_data.tg_id))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "User with this Telegram ID already exists")

    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

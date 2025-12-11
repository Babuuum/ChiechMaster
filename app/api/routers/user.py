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


class UserActivate(UserBase):
    tg_id: int = Field(..., gt=0)


@router.get('/user_list')
async def get_user_list(session: SessionDep):
    stmt = select(User)
    user_list = session.scalars(stmt)
    return {'users' : user_list}

@router.post('/create')
async def create_user(session: SessionDep, user_data=UserCreate):
    existing = await session.execute(select(User).where(User.tg_id == user_data.tg_id))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "User with this Telegram ID already exists")

    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

@router.patch('/activate')
async def deactivate_user(
    user_data: UserActivate,
    session: SessionDep
):
    stmt = select(User).where(User.tg_id == user_data.tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с таким Telegram ID не найден"
        )

    if user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже активен"
        )

    user.is_active = True
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

@router.patch('/deactivate')
async def deactivate_user(session: SessionDep, user_data=UserActivate):
    stmt = select(User).where(User.tg_id == user_data.tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с таким Telegram ID не найден"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Пользователь уже деактивирован"
        )

    user.is_active = False
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

from fastapi import APIRouter
from sqlalchemy import select

from app.core.db.models import User
from app.core.db.session import get_session

router = APIRouter(tags=['/user'])

session = get_session()


@router.get('/users')
async def get_user_list():
    stmt = select(User)
    user_list = session.scalars(stmt).all()
    return {'users' : user_list}

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.chiech_master import League


class LeagueServices:
    @staticmethod
    async def get_actual_leagues(session: AsyncSession) -> League | None:
        league = await session.execute(select(League).where(League.active==True))
        return league.scalar_one_or_none()

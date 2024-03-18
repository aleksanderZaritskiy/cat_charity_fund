from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_donations_by_user_id(
        self, user_id: int, session: AsyncSession
    ) -> Optional[list[Donation]]:

        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return donations.scalars().all()

    async def get_open_donations(
        self, session: AsyncSession
    ) -> Optional[list[Donation]]:

        donations = await session.execute(
            select(Donation).where(Donation.close_date.is_(None))
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_id_by_name(
        self, name: str, session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        project_id = project_id.scalars().all()
        return project_id

    async def get_open_projects(
        self, session: AsyncSession
    ) -> Optional[list[CharityProject]]:

        projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.close_date.is_(None))
            .order_by(CharityProject.create_date)
        )
        return projects.scalars().all()


charityproject_crud = CRUDCharityProject(CharityProject)

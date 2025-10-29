from typing import Iterable

from sqlalchemy import select

from .base import BaseRepository
from ..models.writing_principle import WritingPrinciple


class WritingPrincipleRepository(BaseRepository[WritingPrinciple]):
    model = WritingPrinciple

    async def get_enabled_by_project_id(self, project_id: str) -> Iterable[WritingPrinciple]:
        """
        Retrieves all enabled writing principles for a given project.
        """
        stmt = (
            select(WritingPrinciple)
            .where(
                WritingPrinciple.project_id == project_id,
                WritingPrinciple.is_enabled == True
            )
            .order_by(WritingPrinciple.id.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_project_id(self, project_id: str) -> Iterable[WritingPrinciple]:
        """
        Retrieves all writing principles for a given project.
        """
        stmt = (
            select(WritingPrinciple)
            .where(WritingPrinciple.project_id == project_id)
            .order_by(WritingPrinciple.id.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
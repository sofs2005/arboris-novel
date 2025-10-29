from typing import Iterable

from sqlalchemy import select

from .base import BaseRepository
from ..models.plot_arc import PlotArc


class PlotArcRepository(BaseRepository[PlotArc]):
    model = PlotArc

    async def get_unresolved_by_project_id(self, project_id: str) -> Iterable[PlotArc]:
        """
        Retrieves all unresolved plot arcs for a given project.
        """
        stmt = (
            select(PlotArc)
            .where(
                PlotArc.project_id == project_id,
                PlotArc.status == "unresolved"
            )
            .order_by(PlotArc.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_project_id(self, project_id: str) -> Iterable[PlotArc]:
        """
        Retrieves all plot arcs for a given project.
        """
        stmt = (
            select(PlotArc)
            .where(PlotArc.project_id == project_id)
            .order_by(PlotArc.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
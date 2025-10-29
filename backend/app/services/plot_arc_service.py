from __future__ import annotations

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..models.plot_arc import PlotArc
from ..repositories.plot_arc_repository import PlotArcRepository
from ..schemas.plot_arc import PlotArcCreate, PlotArcUpdate


class PlotArcService:
    """Service for managing plot arcs."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = PlotArcRepository(session)

    async def get_plot_arc(self, plot_arc_id: int) -> Optional[PlotArc]:
        return await self.repo.get_by_id(plot_arc_id)

    async def get_plot_arcs_for_project(self, project_id: str) -> List[PlotArc]:
        return await self.repo.get_by_project_id(project_id) # This method needs to be added to the repo

    async def create_plot_arc(self, project_id: str, plot_arc_in: PlotArcCreate) -> PlotArc:
        plot_arc = PlotArc(**plot_arc_in.model_dump(), project_id=project_id)
        self.session.add(plot_arc)
        await self.session.commit()
        await self.session.refresh(plot_arc)
        return plot_arc

    async def update_plot_arc(self, plot_arc_id: int, plot_arc_in: PlotArcUpdate) -> PlotArc:
        plot_arc = await self.get_plot_arc(plot_arc_id)
        if not plot_arc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plot arc not found")
        
        update_data = plot_arc_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(plot_arc, key, value)
            
        await self.session.commit()
        await self.session.refresh(plot_arc)
        return plot_arc

    async def delete_plot_arc(self, plot_arc_id: int) -> None:
        plot_arc = await self.get_plot_arc(plot_arc_id)
        if not plot_arc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plot arc not found")
        
        await self.session.delete(plot_arc)
        await self.session.commit()
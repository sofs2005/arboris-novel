from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.dependencies import get_current_user
from ...db.session import get_session
from ...schemas.plot_arc import PlotArc, PlotArcCreate, PlotArcUpdate
from ...schemas.user import UserInDB
from ...services.novel_service import NovelService
from ...services.plot_arc_service import PlotArcService

router = APIRouter(prefix="/api/novels/{project_id}/plot-arcs", tags=["Plot Arcs"])


async def get_plot_arc_service(session: AsyncSession = Depends(get_session)) -> PlotArcService:
    return PlotArcService(session)


async def get_novel_service(session: AsyncSession = Depends(get_session)) -> NovelService:
    return NovelService(session)


@router.post("", response_model=PlotArc, status_code=status.HTTP_201_CREATED)
async def create_plot_arc(
    project_id: str,
    plot_arc_in: PlotArcCreate,
    service: PlotArcService = Depends(get_plot_arc_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
) -> PlotArc:
    await novel_service.ensure_project_owner(project_id, current_user.id)
    return await service.create_plot_arc(project_id, plot_arc_in)


@router.get("", response_model=List[PlotArc])
async def get_plot_arcs(
    project_id: str,
    service: PlotArcService = Depends(get_plot_arc_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
) -> List[PlotArc]:
    await novel_service.ensure_project_owner(project_id, current_user.id)
    return await service.get_plot_arcs_for_project(project_id)


@router.put("/{plot_arc_id}", response_model=PlotArc)
async def update_plot_arc(
    project_id: str,
    plot_arc_id: int,
    plot_arc_in: PlotArcUpdate,
    service: PlotArcService = Depends(get_plot_arc_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
) -> PlotArc:
    await novel_service.ensure_project_owner(project_id, current_user.id)
    # Further check if plot_arc belongs to the project can be added here
    return await service.update_plot_arc(plot_arc_id, plot_arc_in)


@router.delete("/{plot_arc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plot_arc(
    project_id: str,
    plot_arc_id: int,
    service: PlotArcService = Depends(get_plot_arc_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
):
    await novel_service.ensure_project_owner(project_id, current_user.id)
    # Further check if plot_arc belongs to the project can be added here
    await service.delete_plot_arc(plot_arc_id)
    return None
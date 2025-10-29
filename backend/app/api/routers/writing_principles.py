from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.dependencies import get_current_user
from ...db.session import get_session
from ...schemas.writing_principle import WritingPrinciple, WritingPrincipleCreate, WritingPrincipleUpdate
from ...schemas.user import UserInDB
from ...services.novel_service import NovelService
from ...services.writing_principle_service import WritingPrincipleService

router = APIRouter(prefix="/api/novels/{project_id}/writing-principles", tags=["Writing Principles"])


async def get_writing_principle_service(session: AsyncSession = Depends(get_session)) -> WritingPrincipleService:
    return WritingPrincipleService(session)


async def get_novel_service(session: AsyncSession = Depends(get_session)) -> NovelService:
    return NovelService(session)


@router.post("", response_model=WritingPrinciple, status_code=status.HTTP_201_CREATED)
async def create_writing_principle(
    project_id: str,
    principle_in: WritingPrincipleCreate,
    service: WritingPrincipleService = Depends(get_writing_principle_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
) -> WritingPrinciple:
    await novel_service.ensure_project_owner(project_id, current_user.id)
    return await service.create_writing_principle(project_id, principle_in)


@router.get("", response_model=List[WritingPrinciple])
async def get_writing_principles(
    project_id: str,
    service: WritingPrincipleService = Depends(get_writing_principle_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
) -> List[WritingPrinciple]:
    await novel_service.ensure_project_owner(project_id, current_user.id)
    return await service.get_writing_principles_for_project(project_id)


@router.put("/{principle_id}", response_model=WritingPrinciple)
async def update_writing_principle(
    project_id: str,
    principle_id: int,
    principle_in: WritingPrincipleUpdate,
    service: WritingPrincipleService = Depends(get_writing_principle_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
) -> WritingPrinciple:
    await novel_service.ensure_project_owner(project_id, current_user.id)
    # Further check if principle belongs to the project can be added here
    return await service.update_writing_principle(principle_id, principle_in)


@router.delete("/{principle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_writing_principle(
    project_id: str,
    principle_id: int,
    service: WritingPrincipleService = Depends(get_writing_principle_service),
    novel_service: NovelService = Depends(get_novel_service),
    current_user: UserInDB = Depends(get_current_user),
):
    await novel_service.ensure_project_owner(project_id, current_user.id)
    # Further check if principle belongs to the project can be added here
    await service.delete_writing_principle(principle_id)
    return None
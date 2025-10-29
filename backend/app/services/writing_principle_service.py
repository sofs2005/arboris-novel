from __future__ import annotations

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from ..models.writing_principle import WritingPrinciple
from ..repositories.writing_principle_repository import WritingPrincipleRepository
from ..schemas.writing_principle import WritingPrincipleCreate, WritingPrincipleUpdate


class WritingPrincipleService:
    """Service for managing writing principles."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = WritingPrincipleRepository(session)

    async def get_writing_principle(self, principle_id: int) -> Optional[WritingPrinciple]:
        return await self.repo.get_by_id(principle_id)

    async def get_writing_principles_for_project(self, project_id: str) -> List[WritingPrinciple]:
        return await self.repo.get_by_project_id(project_id) # This method needs to be added to the repo

    async def create_writing_principle(self, project_id: str, principle_in: WritingPrincipleCreate) -> WritingPrinciple:
        principle = WritingPrinciple(**principle_in.model_dump(), project_id=project_id)
        self.session.add(principle)
        await self.session.commit()
        await self.session.refresh(principle)
        return principle

    async def update_writing_principle(self, principle_id: int, principle_in: WritingPrincipleUpdate) -> WritingPrinciple:
        principle = await self.get_writing_principle(principle_id)
        if not principle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writing principle not found")
        
        update_data = principle_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(principle, key, value)
            
        await self.session.commit()
        await self.session.refresh(principle)
        return principle

    async def delete_writing_principle(self, principle_id: int) -> None:
        principle = await self.get_writing_principle(principle_id)
        if not principle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Writing principle not found")
        
        await self.session.delete(principle)
        await self.session.commit()
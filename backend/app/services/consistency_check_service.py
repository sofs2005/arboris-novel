from __future__ import annotations

from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.novel import Chapter, NovelProject
from ..repositories.novel_repository import NovelRepository
from ..repositories.plot_arc_repository import PlotArcRepository # Assuming this will be created
from .llm_service import LLMService

CONSISTENCY_PROMPT = """\
Please act as a professional novel editor. Your task is to check for any significant conflicts or inconsistencies between the latest chapter and the established settings of the novel. Please also point out if any unresolved plot points are being ignored or need to be advanced.

Here is the context:

- Novel Setting:
{novel_setting}

- Main Characters' Status:
{character_state}

- Previous Chapters Summary:
{global_summary}

- Unresolved Plot Points / Arcs:
{plot_arcs}

- Latest Chapter Content:
{chapter_text}

Please list any conflicts or inconsistencies you find. If there are none, please return "No significant inconsistencies found."
"""


class ConsistencyCheckService:
    """A service to check for narrative consistency in a novel chapter."""

    def __init__(self, session: AsyncSession, llm_service: LLMService):
        self.session = session
        self.llm_service = llm_service
        self.novel_repo = NovelRepository(session)
        self.plot_arc_repo = PlotArcRepository(session) # Assuming this will be created

    async def check_chapter_consistency(self, project: NovelProject, chapter: Chapter) -> str:
        """
        Checks the consistency of a given chapter against the novel's context.

        Args:
            project: The novel project.
            chapter: The chapter to be checked.

        Returns:
            A string containing the consistency analysis from the LLM.
        """
        context = await self._gather_context(project, chapter)
        
        prompt = CONSISTENCY_PROMPT.format(
            novel_setting=context.get("novel_setting", "Not available."),
            character_state=context.get("character_state", "Not available."),
            global_summary=context.get("global_summary", "Not available."),
            plot_arcs=context.get("plot_arcs", "None."),
            chapter_text=context.get("chapter_text", "")
        )

        response = await self.llm_service.generate_text(prompt, max_tokens=2048, temperature=0.3)
        return response or "The consistency check agent did not provide a response."

    async def _gather_context(self, project: NovelProject, chapter: Chapter) -> Dict[str, Any]:
        """Gathers all necessary context for the consistency check."""
        
        # 1. Novel Setting from Blueprint
        blueprint = project.blueprint
        novel_setting_parts = []
        if blueprint:
            if blueprint.one_sentence_summary:
                novel_setting_parts.append(f"One Sentence Summary: {blueprint.one_sentence_summary}")
            if blueprint.full_synopsis:
                novel_setting_parts.append(f"Full Synopsis: {blueprint.full_synopsis}")
            if blueprint.world_setting:
                novel_setting_parts.append(f"World Setting: {blueprint.world_setting}")
        
        # 2. Character States
        characters = sorted(project.characters, key=lambda c: c.position)
        character_state = "\n".join([f"- {c.name}: {c.identity}. Goals: {c.goals}" for c in characters])

        # 3. Global Summary (Previous Chapters)
        # For now, we'll use a simple summary of the last few chapters.
        # A more advanced implementation would generate and store summaries for each chapter.
        previous_chapters = [ch for ch in sorted(project.chapters, key=lambda c: c.chapter_number) if ch.chapter_number < chapter.chapter_number and ch.selected_version]
        recent_chapters = previous_chapters[-3:] # Get last 3 chapters
        global_summary = "\n".join([f"Chapter {c.chapter_number}: {c.real_summary or c.selected_version.content[:200]}..." for c in recent_chapters])

        # 4. Unresolved Plot Arcs
        unresolved_arcs = await self.plot_arc_repo.get_unresolved_by_project_id(project.id)
        plot_arcs = "\n".join([f"- {arc.description}" for arc in unresolved_arcs]) if unresolved_arcs else "None."

        # 5. Chapter Text
        chapter_text = chapter.selected_version.content if chapter.selected_version else ""

        return {
            "novel_setting": "\n".join(novel_setting_parts) if novel_setting_parts else "Not defined.",
            "character_state": character_state or "No characters defined.",
            "global_summary": global_summary or "No previous chapters.",
            "plot_arcs": plot_arcs,
            "chapter_text": chapter_text
        }
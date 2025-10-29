from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.novel import Chapter, NovelProject
from ..models.writing_principle import WritingPrinciple
from ..repositories.writing_principle_repository import WritingPrincipleRepository # Assuming this will be created
from .llm_service import LLMService

EVALUATION_PROMPT = """\
Please act as a professional writing coach. Your task is to evaluate a novel chapter based on a set of established writing principles. For each principle, provide a brief analysis and a score from 1 to 10.

Here are the writing principles to evaluate against:
{writing_principles}

Here is the chapter content to evaluate:
{chapter_text}

Please provide your evaluation in a structured format, addressing each principle separately. Conclude with a summary of the chapter's main strengths and areas for improvement.
"""


class WritingEvaluationService:
    """A service to evaluate a chapter against defined writing principles."""

    def __init__(self, session: AsyncSession, llm_service: LLMService):
        self.session = session
        self.llm_service = llm_service
        self.principle_repo = WritingPrincipleRepository(session) # Assuming this will be created

    async def evaluate_chapter(self, project: NovelProject, chapter: Chapter) -> str:
        """
        Evaluates a chapter using the project's enabled writing principles.

        Args:
            project: The novel project.
            chapter: The chapter to be evaluated.

        Returns:
            A string containing the writing evaluation from the LLM.
        """
        principles = await self.principle_repo.get_enabled_by_project_id(project.id)
        if not principles:
            return "No writing principles are enabled for this project. Evaluation cannot be performed."

        principles_text = self._format_principles_for_prompt(principles)
        chapter_text = chapter.selected_version.content if chapter.selected_version else ""

        if not chapter_text:
            return "Chapter content is empty. Evaluation cannot be performed."

        prompt = EVALUATION_PROMPT.format(
            writing_principles=principles_text,
            chapter_text=chapter_text
        )

        response = await self.llm_service.generate_text(prompt, max_tokens=2048, temperature=0.5)
        return response or "The writing evaluation agent did not provide a response."

    def _format_principles_for_prompt(self, principles: List[WritingPrinciple]) -> str:
        """Formats the list of principles into a string for the LLM prompt."""
        formatted_principles = []
        for p in principles:
            formatted_principles.append(
                f"- Topic: {p.risk_topic}\n"
                f"  - Core Problem: {p.core_problem}\n"
                f"  - Guiding Principle: {p.guiding_principle}"
            )
        return "\n".join(formatted_principles)
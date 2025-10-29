from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base
from .novel import BIGINT_PK_TYPE, NovelProject, Chapter


class PlotArc(Base):
    """剧情弧光/伏笔表"""

    __tablename__ = "plot_arcs"

    id: Mapped[int] = mapped_column(BIGINT_PK_TYPE, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("novel_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="unresolved", nullable=False) # unresolved, resolved

    start_chapter_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chapters.id", ondelete="SET NULL"))
    resolved_chapter_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chapters.id", ondelete="SET NULL"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project: Mapped["NovelProject"] = relationship()
    start_chapter: Mapped[Optional["Chapter"]] = relationship(foreign_keys=[start_chapter_id])
    resolved_chapter: Mapped[Optional["Chapter"]] = relationship(foreign_keys=[resolved_chapter_id])
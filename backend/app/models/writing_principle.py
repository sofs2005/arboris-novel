from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base
from .novel import BIGINT_PK_TYPE, NovelProject


class WritingPrinciple(Base):
    """写作原则/写作宪法表"""

    __tablename__ = "writing_principles"

    id: Mapped[int] = mapped_column(BIGINT_PK_TYPE, primary_key=True, autoincrement=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("novel_projects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    risk_topic: Mapped[str] = mapped_column(String(255), nullable=False)
    core_problem: Mapped[str] = mapped_column(Text)
    guiding_principle: Mapped[str] = mapped_column(Text)
    macro_strategy: Mapped[str] = mapped_column(Text)
    micro_strategy: Mapped[str] = mapped_column(Text)
    
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project: Mapped["NovelProject"] = relationship()
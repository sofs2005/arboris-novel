from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base_class import Base


class UpdateLog(Base):
    """更新日志表，供公告与后台管理使用。"""

    __tablename__ = "update_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[str | None] = mapped_column(String(64))
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

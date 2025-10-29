from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class LLMConfig(Base):
    """用户自定义的 LLM 接入配置。"""

    __tablename__ = "llm_configs"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    llm_provider_url: Mapped[str | None] = mapped_column(Text())
    llm_provider_api_key: Mapped[str | None] = mapped_column(Text())
    llm_provider_model: Mapped[str | None] = mapped_column(Text())

    user: Mapped["User"] = relationship("User", back_populates="llm_config")

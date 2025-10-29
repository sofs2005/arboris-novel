# ruff: noqa: F401
from sqlalchemy.orm import DeclarativeBase, declared_attr

# Import all models here for Alembic auto-detection
from ..models.admin_setting import AdminSetting
from ..models.llm_config import LLMConfig
from ..models.novel import (
    BlueprintCharacter,
    BlueprintRelationship,
    Chapter,
    ChapterEvaluation,
    ChapterOutline,
    ChapterVersion,
    NovelBlueprint,
    NovelConversation,
    NovelProject,
)
from ..models.plot_arc import PlotArc
from ..models.prompt import Prompt
from ..models.system_config import SystemConfig
from ..models.update_log import UpdateLog
from ..models.usage_metric import UsageMetric, UserDailyRequest
from ..models.user import User
from ..models.writing_principle import WritingPrinciple


class Base(DeclarativeBase):
    """SQLAlchemy 基类，自动根据类名生成表名。"""

    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return cls.__name__.lower()

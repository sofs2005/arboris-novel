# ruff: noqa: F401
# Import all models here for Alembic auto-detection
from .base_class import Base  # noqa: F401
from ..models.admin_setting import AdminSetting  # noqa: F401
from ..models.llm_config import LLMConfig  # noqa: F401
from ..models.novel import (  # noqa: F401
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
from ..models.plot_arc import PlotArc  # noqa: F401
from ..models.prompt import Prompt  # noqa: F401
from ..models.system_config import SystemConfig  # noqa: F401
from ..models.update_log import UpdateLog  # noqa: F401
from ..models.usage_metric import UsageMetric, UserDailyRequest  # noqa: F401
from ..models.user import User  # noqa: F401
from ..models.writing_principle import WritingPrinciple  # noqa: F401

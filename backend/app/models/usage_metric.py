from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base_class import Base


class UsageMetric(Base):
    """通用计数器表，目前用于记录 API 请求次数等统计数据。"""

    __tablename__ = "usage_metrics"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

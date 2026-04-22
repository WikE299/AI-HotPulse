import uuid
from datetime import datetime

from sqlalchemy import String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DailyBrief(Base):
    __tablename__ = "daily_briefs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)  # "2026-04-22"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    article_ids: Mapped[str] = mapped_column(Text, default="[]")  # JSON list
    generated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)

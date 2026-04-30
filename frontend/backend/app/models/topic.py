import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_key: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    article_count: Mapped[int] = mapped_column(Integer, default=1)
    heat_score: Mapped[int] = mapped_column(Integer, default=0)
    representative_id: Mapped[str | None] = mapped_column(String(36))
    first_seen_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    latest_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)

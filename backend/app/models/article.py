import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, ARRAY, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(100))
    source_type: Mapped[str | None] = mapped_column(String(20))  # chinese/english/academic/social
    original_url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    crawled_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    image_url: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    keywords: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    category: Mapped[str | None] = mapped_column(String(50))
    heat_score: Mapped[int] = mapped_column(Integer, default=0)
    content_snippet: Mapped[str | None] = mapped_column(Text)

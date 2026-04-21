import json
import uuid
from datetime import datetime

from sqlalchemy import String, Text, Integer, TIMESTAMP, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JSONList(TypeDecorator):
    """Stores a list as JSON text, compatible with SQLite and PostgreSQL."""
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value else []


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(100))
    source_type: Mapped[str | None] = mapped_column(String(20))
    original_url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    crawled_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    image_url: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)
    keywords: Mapped[list | None] = mapped_column(JSONList)
    category: Mapped[str | None] = mapped_column(String(50))
    heat_score: Mapped[int] = mapped_column(Integer, default=0)
    content_snippet: Mapped[str | None] = mapped_column(Text)

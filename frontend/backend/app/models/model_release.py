import json
import uuid

from sqlalchemy import String, Text, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JSONDict(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value else {}


class ModelRelease(Base):
    __tablename__ = "model_releases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name: Mapped[str] = mapped_column(Text, nullable=False)
    organization: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str | None] = mapped_column(String(50))
    release_date: Mapped[str] = mapped_column(String(10), nullable=False)
    parameters_size: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text)
    benchmarks: Mapped[dict | None] = mapped_column(JSONDict)
    announcement_url: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(30), default="LLM")

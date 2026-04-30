import uuid

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    person_name: Mapped[str] = mapped_column(String(100), nullable=False)
    person_title: Mapped[str] = mapped_column(String(200), nullable=False)
    person_org: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_file: Mapped[str] = mapped_column(String(100), nullable=False)
    quote: Mapped[str] = mapped_column(Text, nullable=False)
    quote_source: Mapped[str | None] = mapped_column(Text)
    quote_date: Mapped[str | None] = mapped_column(String(10))
    deadline: Mapped[str | None] = mapped_column(String(10))
    category: Mapped[str] = mapped_column(String(30), default="capability")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    credibility_note: Mapped[str | None] = mapped_column(Text)

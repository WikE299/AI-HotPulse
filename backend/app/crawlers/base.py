from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RawArticle:
    title: str
    original_url: str
    source: str
    source_type: str  # chinese / english / academic / social
    published_at: datetime | None = None
    image_url: str | None = None
    content_snippet: str | None = None


class BaseCrawler(ABC):
    @abstractmethod
    async def fetch(self) -> list[RawArticle]:
        ...

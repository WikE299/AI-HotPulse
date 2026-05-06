import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "frontend", "backend"))
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/hotpulse.db")

from main import app  # noqa: E402

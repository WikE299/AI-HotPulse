import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Default to /tmp SQLite on Vercel only when no database URL is configured
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/hotpulse.db")

from main import app  # noqa: E402

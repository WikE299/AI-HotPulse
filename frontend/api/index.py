import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Use /tmp for SQLite on Vercel (only writable directory)
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/hotpulse.db"

from main import app  # noqa: E402

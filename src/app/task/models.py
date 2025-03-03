from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from src.app.core.config import settings
from src.app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(settings.TIMEZONE),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(settings.TIMEZONE),
        onupdate=lambda: datetime.now(settings.TIMEZONE),
        nullable=False,
    )
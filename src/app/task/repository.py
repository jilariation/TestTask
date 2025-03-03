import typing
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.config import settings
from src.app.task import models
from src.app.task.models import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> typing.List[models.Task]:
        result = await self.db.execute(select(models.Task))
        return result.scalars().all()

    async def get_by_id(self, task_id: int) -> typing.Optional[models.Task]:
        result = await self.db.execute(
            select(models.Task)
            .where(models.Task.id == task_id)
        )
        return result.scalars().first()

    async def create(self, task_data: dict[str, typing.Any]) -> models.Task:
        task = Task(**task_data)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update(self, task_id: int, task_data: dict[str, typing.Any]) -> typing.Optional[models.Task]:
        task_data['updated_at'] = datetime.now(settings.TIMEZONE)

        await self.db.execute(
            update(models.Task)
            .where(models.Task.id == task_id)
            .values(**task_data)
        )
        await self.db.commit()

        return await self.get_by_id(task_id)

    async def delete(self, task_id: int) -> None:
        await self.db.execute(
            delete(models.Task)
            .where(models.Task.id == task_id)
        )
        await self.db.commit()
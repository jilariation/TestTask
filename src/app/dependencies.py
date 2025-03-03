from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.task import repository
from src.app.task.repository import TaskRepository
from src.app.task.service import TaskService


async def get_task_repository(db: AsyncSession = Depends(get_db)) -> repository.TaskRepository:
    return TaskRepository(db)

async def get_task_service(
    task_repository: repository.TaskRepository = Depends(get_task_repository)
) -> TaskService:
    return TaskService(task_repository)
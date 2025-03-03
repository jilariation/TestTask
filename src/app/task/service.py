import typing

from fastapi import HTTPException, status

from src.app.core.logging import logger
from src.app.core.mapper import DTOMapper
from src.app.task import schemas
from src.app.task.repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def get_all_tasks(self) -> typing.List[schemas.TaskResponse]:
        logger.info("Fetching all tasks")
        tasks = await self.task_repository.get_all()
        logger.info(f"Retrieved {len(tasks)} tasks")

        return DTOMapper.tasks_to_responses(tasks)

    async def get_task_by_id(self, task_id: int) -> schemas.TaskResponse:
        logger.info(f"Fetching task with ID {task_id}")
        task = await self.task_repository.get_by_id(task_id)

        if not task:
            logger.warning(f"Task with ID {task_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        logger.info(f"Retrieved task with ID {task_id}")

        return DTOMapper.task_to_response(task) #task_data.model_dump()

    async def create_task(self, task_data: schemas.TaskCreate) -> schemas.TaskResponse:
        logger.info(f"Creating new task: {task_data.title}")
        task_dict = DTOMapper.create_dto_to_dict(task_data)
        task = await self.task_repository.create(task_dict)
        logger.info(f"Created new task with ID {task.id}")

        return DTOMapper.task_to_response(task)

    async def update_task(self, task_id: int, task_data: schemas.TaskUpdate) -> schemas.TaskResponse:
        logger.info(f"Updating task with ID {task_id}")

        await self.get_task_by_id(task_id)

        task_dict = DTOMapper.update_dto_to_dict(task_data)
        updated_task = await self.task_repository.update(task_id, task_dict)

        if not updated_task:
            logger.warning(f"Task with ID {task_id} not found during update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        logger.info(f"Updated task with ID {task_id}")

        return DTOMapper.task_to_response(updated_task)

    async def delete_task(self, task_id: int) -> None:
        logger.info(f"Deleting task with ID {task_id}")

        await self.get_task_by_id(task_id)

        await self.task_repository.delete(task_id)

        logger.info(f"Deleted task with ID {task_id}")
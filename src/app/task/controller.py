import typing

from fastapi import APIRouter, Depends, status, Response

from src.app.core.logging import logger
from src.app.dependencies import get_task_service
from src.app.task import schemas
from src.app.task.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=typing.List[schemas.TaskResponse], status_code=status.HTTP_200_OK)
async def get_all_tasks(
        task_service: TaskService = Depends(get_task_service)
) -> typing.List[schemas.TaskResponse]:
    logger.info("API request: GET /tasks")
    return await task_service.get_all_tasks()


@router.get("/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
        task_id: int,
        task_service: TaskService = Depends(get_task_service)
) -> schemas.TaskResponse:
    logger.info(f"API request: GET /tasks/{task_id}")
    return await task_service.get_task_by_id(task_id)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(
        task_data: schemas.TaskCreate,
        task_service: TaskService = Depends(get_task_service)
) -> dict:
    logger.info(f"API request: POST /tasks with data {task_data.model_dump()}")
    task = await task_service.create_task(task_data)
    return {"id": task.id}


@router.put("/update/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
        task_id: int,
        task_data: schemas.TaskUpdate,
        task_service: TaskService = Depends(get_task_service)
) ->  schemas.TaskResponse:
    logger.info(f"API request: PUT /tasks/{task_id} with data {task_data.model_dump()}")
    return await task_service.update_task(task_id, task_data)


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_service: TaskService = Depends(get_task_service)
) -> Response:
    logger.info(f"API request: DELETE /tasks/{task_id}")
    await task_service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
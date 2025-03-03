from datetime import datetime
from typing import Generator
from unittest.mock import AsyncMock, patch

import pytest
from starlette.testclient import TestClient

from . import app
from src.app.core.config import settings
from src.app.task.models import Task
from src.app.task.repository import TaskRepository
from src.app.task.schemas import TaskResponse
from src.app.task.service import TaskService


@pytest.fixture
def mock_datetime_now():
    fixed_now = datetime(2025, 3, 2, 12, 0, 0, tzinfo=settings.TIMEZONE)
    with patch('src.app.task.repository.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_now
        yield mock_datetime


@pytest.fixture
def task_sample():
    now = datetime.now(settings.TIMEZONE)
    return Task(
        id=1,
        title="Test Task",
        description="Test Description",
        created_at=now,
        updated_at=now
    )


@pytest.fixture
def task_samples():
    now = datetime.now(settings.TIMEZONE)
    return [
        Task(
            id=1,
            title="Task 1",
            description="Description for Task 1",
            created_at=now,
            updated_at=now
        ),
        Task(
            id=2,
            title="Task 2",
            description="Description for Task 2",
            created_at=now,
            updated_at=now
        ),
        Task(
            id=3,
            title="Task 3",
            description="Description for Task 3",
            created_at=now,
            updated_at=now
        )
    ]


@pytest.fixture
def task_response_sample():
    now = datetime.now(settings.TIMEZONE)
    return TaskResponse(
        id=1,
        title="Test Task",
        description="Test Description",
        created_at=now,
        updated_at=now
    )


@pytest.fixture
def task_response_samples():
    now = datetime.now(settings.TIMEZONE)
    return [
        TaskResponse(
            id=1,
            title="Task 1",
            description="Description for Task 1",
            created_at=now,
            updated_at=now
        ),
        TaskResponse(
            id=2,
            title="Task 2",
            description="Description for Task 2",
            created_at=now,
            updated_at=now
        ),
        TaskResponse(
            id=3,
            title="Task 3",
            description="Description for Task 3",
            created_at=now,
            updated_at=now
        )
    ]


@pytest.fixture
def mock_db_session():
    session = AsyncMock()

    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()

    session.execute = AsyncMock()
    session.refresh = AsyncMock()

    return session


@pytest.fixture
def mock_task_repository(task_sample, task_samples):
    repository_mock = AsyncMock(spec=TaskRepository)

    repository_mock.get_all.return_value = task_samples
    repository_mock.get_by_id.side_effect = lambda task_id: (
        next((t for t in task_samples if t.id == task_id), None)
    )
    repository_mock.create.return_value = task_sample
    repository_mock.update.side_effect = lambda task_id, task_data: (
        task_sample if task_id == 1 else None
    )
    repository_mock.delete.return_value = None

    return repository_mock


@pytest.fixture
def mock_task_service(task_response_sample, task_response_samples):
    service_mock = AsyncMock(spec=TaskService)

    service_mock.get_all_tasks.return_value = task_response_samples
    service_mock.get_task_by_id.side_effect = lambda task_id: (
        task_response_sample if task_id == 1 else (_ for _ in ()).throw(Exception("Task not found"))
    )
    service_mock.create_task.return_value = task_response_sample
    service_mock.update_task.side_effect = lambda task_id, task_data: (
        task_response_sample if task_id == 1 else (_ for _ in ()).throw(Exception("Task not found"))
    )
    service_mock.delete_task.side_effect = lambda task_id: (
        None if task_id == 1 else (_ for _ in ()).throw(Exception("Task not found"))
    )

    return service_mock


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


# Patch app dependencies
@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch, mock_task_service):

    async def _get_task_service():
        return mock_task_service

    with patch('src.app.dependencies.get_task_service', _get_task_service):
        yield
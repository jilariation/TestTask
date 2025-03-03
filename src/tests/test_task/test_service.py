from unittest.mock import patch

import pytest
from fastapi import HTTPException
from unittest.mock import ANY

from src.app.core.mapper import DTOMapper
from src.app.task.schemas import TaskCreate, TaskUpdate
from src.app.task.service import TaskService


@pytest.mark.asyncio
async def test_get_all_tasks(mock_task_repository, task_samples):
    service = TaskService(mock_task_repository)

    with patch.object(DTOMapper, 'tasks_to_responses', return_value=task_samples) as mock_mapper:
        tasks = await service.get_all_tasks()

        mock_task_repository.get_all.assert_called_once()
        mock_mapper.assert_called_once_with(task_samples)
        assert tasks == task_samples


@pytest.mark.asyncio
async def test_get_task_by_id(mock_task_repository, task_sample):
    service = TaskService(mock_task_repository)
    task_id = 1

    mock_task_repository.get_by_id.return_value = task_sample

    with patch.object(DTOMapper, 'task_to_response', return_value=task_sample) as mock_mapper:
        task = await service.get_task_by_id(task_id)

        mock_task_repository.get_by_id.assert_called_once_with(task_id)
        mock_mapper.assert_called_once_with(ANY)
        assert task == task_sample


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(mock_task_repository):
    service = TaskService(mock_task_repository)
    task_id = 999
    mock_task_repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        await service.get_task_by_id(task_id)

    assert excinfo.value.status_code == 404
    mock_task_repository.get_by_id.assert_called_once_with(task_id)


@pytest.mark.asyncio
async def test_create_task(mock_task_repository, task_sample):
    service = TaskService(mock_task_repository)
    task_data = TaskCreate(title="New Task", description="New Description")

    with patch.object(DTOMapper, 'create_dto_to_dict',
                      return_value={"title": "New Task", "description": "New Description"}) as mock_to_dict:
        with patch.object(DTOMapper, 'task_to_response', return_value=task_sample) as mock_to_response:
            task = await service.create_task(task_data)

            mock_to_dict.assert_called_once_with(task_data)
            mock_task_repository.create.assert_called_once_with({"title": "New Task", "description": "New Description"})
            mock_to_response.assert_called_once_with(task_sample)
            assert task == task_sample


@pytest.mark.asyncio
async def test_update_task(mock_task_repository, task_sample):
    service = TaskService(mock_task_repository)
    task_id = 1
    update_data = TaskUpdate(title="Updated Task", description="Updated Description")

    with patch.object(service, 'get_task_by_id', return_value=True) as mock_get:
        with patch.object(DTOMapper, 'update_dto_to_dict',
                          return_value={"title": "Updated Task", "description": "Updated Description"}) as mock_to_dict:
            with patch.object(DTOMapper, 'task_to_response', return_value=task_sample) as mock_to_response:
                updated_task = await service.update_task(task_id, update_data)

                mock_get.assert_called_once_with(task_id)
                mock_to_dict.assert_called_once_with(update_data)
                mock_task_repository.update.assert_called_once_with(task_id, {"title": "Updated Task",
                                                                              "description": "Updated Description"})
                mock_to_response.assert_called_once_with(task_sample)
                assert updated_task == task_sample


@pytest.mark.asyncio
async def test_update_task_not_found(mock_task_repository):
    service = TaskService(mock_task_repository)
    task_id = 999
    update_data = TaskUpdate(title="Updated Task", description="Updated Description")

    with patch.object(service, 'get_task_by_id') as mock_get:
        mock_get.side_effect = HTTPException(status_code=404, detail="Task not found")

        with pytest.raises(HTTPException) as excinfo:
            await service.update_task(task_id, update_data)

        assert excinfo.value.status_code == 404
        mock_get.assert_called_once_with(task_id)
        mock_task_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_delete_task(mock_task_repository):
    service = TaskService(mock_task_repository)
    task_id = 1

    with patch.object(service, 'get_task_by_id', return_value=True) as mock_get:
        await service.delete_task(task_id)

        mock_get.assert_called_once_with(task_id)
        mock_task_repository.delete.assert_called_once_with(task_id)


@pytest.mark.asyncio
async def test_delete_task_not_found(mock_task_repository):
    service = TaskService(mock_task_repository)
    task_id = 999

    with patch.object(service, 'get_task_by_id') as mock_get:
        mock_get.side_effect = HTTPException(status_code=404, detail="Task not found")

        with pytest.raises(HTTPException) as excinfo:
            await service.delete_task(task_id)

        assert excinfo.value.status_code == 404
        mock_get.assert_called_once_with(task_id)
        mock_task_repository.delete.assert_not_called()
from unittest.mock import AsyncMock, patch

import pytest

from src.app.task.repository import TaskRepository


@pytest.mark.asyncio
async def test_get_all(mock_db_session, task_samples):
    repository = TaskRepository(mock_db_session)

    # Попытка в SQL запрос, ненавижу асинхронные тесты
    class MockQueryResult:
        def scalars(self):
            class MockScalars:
                def all(self):
                    return task_samples

            return MockScalars()

    async def mock_execute(*args, **kwargs):
        return MockQueryResult()

    mock_db_session.execute = mock_execute

    tasks = await repository.get_all()

    assert tasks == task_samples


@pytest.mark.asyncio
async def test_get_by_id(mock_db_session, task_sample):
    repository = TaskRepository(mock_db_session)
    task_id = 1

    class MockQueryResult:
        def scalars(self):
            class MockScalars:
                def first(self):
                    return task_sample

            return MockScalars()

    async def mock_execute(*args, **kwargs):
        return MockQueryResult()

    mock_db_session.execute = mock_execute

    task = await repository.get_by_id(task_id)

    assert task == task_sample


@pytest.mark.asyncio
async def test_get_by_id_not_found(mock_db_session):
    repository = TaskRepository(mock_db_session)
    task_id = 999

    class MockQueryResult:
        def scalars(self):
            class MockScalars:
                def first(self):
                    return None

            return MockScalars()

    async def mock_execute(*args, **kwargs):
        return MockQueryResult()

    mock_db_session.execute = mock_execute

    task = await repository.get_by_id(task_id)

    assert task is None


@pytest.mark.asyncio
async def test_create(mock_db_session, task_sample, mock_datetime_now):
    repository = TaskRepository(mock_db_session)
    task_data = {
        "title": "New Task",
        "description": "New Description"
    }

    with patch('src.app.task.repository.Task', return_value=task_sample):
        task = await repository.create(task_data)

        mock_db_session.add.assert_called_once_with(task_sample)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(task_sample)
        assert task == task_sample


@pytest.mark.asyncio
async def test_update(mock_db_session, task_sample, mock_datetime_now):
    repository = TaskRepository(mock_db_session)
    task_id = 1
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description"
    }

    mock_execute_result = AsyncMock()
    mock_db_session.execute = AsyncMock(return_value=mock_execute_result)

    with patch.object(repository, 'get_by_id', return_value=task_sample):
        updated_task = await repository.update(task_id, update_data)

        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()
        assert updated_task == task_sample


@pytest.mark.asyncio
async def test_update_not_found(mock_db_session, mock_datetime_now):
    repository = TaskRepository(mock_db_session)
    task_id = 999
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description"
    }

    with patch.object(repository, 'get_by_id', return_value=None) as mock_get:
        updated_task = await repository.update(task_id, update_data)

        assert 'updated_at' in update_data
        assert update_data['updated_at'] == mock_datetime_now.now.return_value

        mock_db_session.execute.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_get.assert_called_once_with(task_id)
        assert updated_task is None


@pytest.mark.asyncio
async def test_delete(mock_db_session):
    repository = TaskRepository(mock_db_session)
    task_id = 1

    await repository.delete(task_id)

    mock_db_session.execute.assert_called_once()
    mock_db_session.commit.assert_called_once()
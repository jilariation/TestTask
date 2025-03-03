# Task Manager API
REST API-сервис на FastAPI для управления списком задач. Проект реализован с использованием асинхронного подхода, имеет чистую архитектуру и полное тестовое покрытие.
## Функциональные возможности

- Получение списка всех задач
- Получение конкретной задачи по ID
- Создание новой задачи
- Обновление существующей задачи
- Удаление задачи
- Асинхронная работа с базой данных SQLite
- Подробное логирование операций

## Стек технологий

- FastAPI - веб-фреймворк для создания API
- SQLAlchemy - ORM для работы с базой данных
- Alembic - система миграций базы данных
- Pydantic - валидация данных и сериализация
- SQLite с асинхронным движком
- Pytest - тестирование

## Установка и запуск
### Требования

- Python 3.8+
- Виртуальное окружение Python (рекомендуется)

### Установка

Клонируйте репозиторий:

```bash
git clone https://github.com/jilariation/TestTask.git
cd TestTask
```

Создайте и активируйте виртуальное окружение:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python -m venv .venv
source .venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Примените миграции базы данных:

```bash
alembic upgrade head
```
### Запуск сервера
```bash
uvicorn main:app --reload
```
API будет доступно по адресу http://127.0.0.1:8080
## Структура проекта
```
TestTask/
├── .venv/                      # Виртуальное окружение Python
├── alembic/                    # Конфигурация и миграции Alembic
│   ├── versions/               # Версии миграций
│   ├── env.py                  # Настройки среды для миграций
│   └── alembic.ini             # Конфигурация Alembic
├── src/
│   ├── app/                    # Основной код приложения
│   │   ├── core/               # Ядро приложения
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # Конфигурация приложения
│   │   │   ├── database.py     # Подключение к БД
│   │   │   ├── logging.py      # Настройка логирования
│   │   │   └── mapper.py       # DTO-маппер
│   │   ├── task/               # Модуль задач
│   │   │   ├── __init__.py
│   │   │   ├── controller.py   # Контроллеры API
│   │   │   ├── models.py       # Модели данных SQLAlchemy
│   │   │   ├── repository.py   # Репозиторий для работы с БД
│   │   │   ├── schemas.py      # Pydantic-схемы
│   │   │   └── service.py      # Бизнес-логика
│   │   └── dependencies.py     # Зависимости FastAPI
│   ├── tests/                  # Тесты
│   │   ├── test_task/          # Тесты модуля задач
│   │   │   ├── test_repo.py    # Тесты репозитория
│   │   │   └── test_service.py # Тесты сервиса
│   │   └── conftest.py         # Фикстуры для тестов
├── main.py                     # Точка входа в приложение
├── README.md                   # Документация проекта
├── requirements.txt            # Зависимости Python
└── test.db                     # База данных SQLite для тестов
```
## API Endpoints
### Получение всех задач
```bash
curl --location 'http://localhost:8080/tasks/'
```
Ответ:
```json
[
  {
    "id": 1,
    "title": "Изучить FastAPI",
    "description": "Пройти туториал по FastAPI",
    "created_at": "2025-03-03T10:00:00",
    "updated_at": "2025-03-03T10:00:00"
  },
  {
    "id": 2,
    "title": "Написать тесты",
    "description": "Добавить unit и integration тесты",
    "created_at": "2025-03-03T11:00:00",
    "updated_at": "2025-03-03T11:00:00"
  }
]
```
### Получение задачи по ID
```bash
curl --location 'http://localhost:8080/tasks/1'
```
Ответ:
```json
{
  "id": 1,
  "title": "Изучить FastAPI",
  "description": "Пройти туториал по FastAPI",
  "created_at": "2025-03-03T10:00:00",
  "updated_at": "2025-03-03T10:00:00"
}
```
### Создание новой задачи
```bash
curl --location 'http://localhost:8080/tasks/create' \
--data '{
    "title": "test_title",
    "description": "test_descritption"
}'
```
Ответ:
```json
{
  "id": 3
}
```
### Обновление задачи
```bash
curl --location --request PUT 'http://localhost:8080/tasks/update/1' \
--header 'Content-Type: application/json' \
--data '{
    "title": "updated_test_title1",
    "description": "test_descritption"
}'
```
Ответ:
```json
{
  "id": 1,
  "title": "Обновленная задача",
  "description": "Обновленное описание задачи",
  "created_at": "2025-03-03T10:00:00",
  "updated_at": "2025-03-03T12:30:45"
}
```
### Удаление задачи
```bash
curl --location --request DELETE 'http://localhost:8080/tasks/delete/1' \
--header 'Content-Type: application/json'
```
## Запуск тестов
```bash
# Запуск всех тестов
pytest

# Запуск тестов с детальным выводом
pytest -v

# Запуск определенных тестов
pytest src/tests/test_task/test_service.py

# Запуск с отчетом о покрытии
pytest --cov=src
```
## Особенности тестирования
Тесты используют моки для изоляции компонентов, что позволяет тестировать каждый уровень приложения независимо:

- Репозиторий: Тестируется с моками базы данных
- Сервис: Тестируется с моками репозитория

При работе с асинхронными моками важно правильно настраивать их поведение:
```python
# Пример правильного мокирования асинхронных методов SQLAlchemy
class MockQueryResult:
    def scalars(self):
        class MockScalars:
            def all(self):
                return task_samples
        return MockScalars()

async def mock_execute(*args, **kwargs):
    return MockQueryResult()

mock_db_session.execute = mock_execute
```
## Документация API
После запуска сервера автоматическая документация API доступна по адресам:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Лицензия
Этот проект распространяется под лицензией MIT License.
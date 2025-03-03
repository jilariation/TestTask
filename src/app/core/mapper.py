import typing

from pydantic import BaseModel

from src.app.task.models import Task
from src.app.task.schemas import TaskResponse, TaskCreate, TaskUpdate

T = typing.TypeVar('T', bound=BaseModel)

class DTOMapper:

    @staticmethod
    def to_dto(obj: typing.Any, dto_class: typing.Type[T]) -> T:
        if isinstance(obj, typing.Dict):
            return dto_class(**obj)
        elif hasattr(obj, "__dict__"):
            return dto_class.model_validate(obj)
        else:
            raise ValueError(f"Cannot convert {type(obj)} to {dto_class}")

    @staticmethod
    def to_dto_list(objs: typing.List[typing.Any], dto_class: typing.Type[T]) -> typing.List[T]:
        return [DTOMapper.to_dto(obj, dto_class) for obj in objs]

    @staticmethod
    def task_to_response(task: Task) -> TaskResponse:
        return TaskResponse.model_validate(task)

    @staticmethod
    def tasks_to_responses(tasks: typing.List[Task]) -> typing.List[TaskResponse]:
        return [DTOMapper.task_to_response(task) for task in tasks]

    @staticmethod
    def create_dto_to_dict(task_dto: TaskCreate) -> typing.Dict[str, typing.Any]:
        return task_dto.model_dump()

    @staticmethod
    def update_dto_to_dict(task_dto: TaskUpdate) -> typing.Dict[str, typing.Any]:
        return task_dto.model_dump(exclude_unset=True)
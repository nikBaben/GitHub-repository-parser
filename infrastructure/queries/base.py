from typing import Any
from enum import Enum
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)


DEFAULT_GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
}
"""Стандартные заголовки для запросов к GitHub API."""


def default_github_headers() -> dict[str, str]:
    """
    Возвращает копию стандартных заголовков GitHub API.

    Используется как default_factory в Pydantic моделях,
    чтобы избежать мутации общего словаря.
    """
    return DEFAULT_GITHUB_HEADERS.copy()


class Sort(Enum):
    """Параметры сортировки для запросов GitHub API."""
    NEWEST = "newest"
    OLDEST = "oldest"
    STARGAZERS = "stargazers"
    CREATED = "created"
    UPDATED = "updated"


class State(Enum):
    """Состояние сущностей GitHub (issues, pull requests)."""
    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"


class Direction(Enum):
    """Направление сортировки результатов."""
    ASC = "asc"
    DESC = "desc"


class DatePriority(Enum):
    """
    Поля даты, используемые для извлечения временных значений
    из ответов GitHub API.
    """
    STARRED_AT = "starred_at"
    CREATED_AT = "created_at"
    COMMIT_AUTHOR_DATE = "commit.author.date"
    COMMIT_COMMITTER_DATE = "commit.committer.date"
    UPDATED_AT = "updated_at"
    PUSHED_AT = "pushed_at"

    def extract_from(self, item: dict[str, Any]) -> Any:
        """
        Извлекает значение даты из словаря ответа GitHub API.
        Поддерживает вложенные структуры через разбиение ключа
        по точке (например: commit.author.date).
        """
        value: Any = item

        for part in self.value.split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(part)

        return value


class GitHubQuery(BaseModel):
    """Базовая модель параметров запроса к GitHub API."""
    per_page: int | None = Field(default=None, ge=1, le=100)
    headers: dict[str, str] = Field(
        default_factory=default_github_headers,
    )

    def to_params(self) -> dict[str, Any]:
        """Преобразует модель запроса в параметры для HTTP-запроса."""
        return self.model_dump(
            exclude_none=True,
            exclude={"cutoff_dt", "stop_field", "headers"},
            mode="json",
        )


class GitHubPaginatedQuery(GitHubQuery):
    """
    Расширенная модель параметров запроса 
    с поддержкой постраничной загрузки
    и фильтрации по дате.
    """
    # Дата отсечения. Все элементы старше этой даты игнорируются.
    cutoff_dt: datetime | None = None 
    # Поле даты, используемое для проверки остановки пагинации.
    stop_field: DatePriority | None = None

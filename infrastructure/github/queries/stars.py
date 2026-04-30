from pydantic import Field

from .base import GitHubPaginatedQuery


def starred_at_headers() -> dict[str, str]:
    """
    Использует специальный media type:
    'application/vnd.github.star+json', который позволяет
    получать не только пользователя, но и дату, когда была поставлена звезда.
    """
    return {
        "Accept": "application/vnd.github.star+json",
    }


class StarsQuery(GitHubPaginatedQuery):
    """"
    Модель запроса получения истории звезд репозитория.
    """
    headers: dict[str, str] = Field(
        default_factory=starred_at_headers,
    )

from .base import Sort, GitHubPaginatedQuery


class ForksQuery(GitHubPaginatedQuery):
    """Модель запроса получения истории форков репозитория."""
    sort: Sort

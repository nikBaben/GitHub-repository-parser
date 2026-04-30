from .base import GitHubPaginatedQuery


class ContributorsQuery(GitHubPaginatedQuery):
    """Модель запроса для получения истории конрибьюторов репозитория."""
    anon: bool = True

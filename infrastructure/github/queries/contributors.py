from .base import GitHubPaginatedQuery


class ContributorsQuery(GitHubPaginatedQuery):
    """Модель запроса получения истории конрибьюторов репозитория."""
    anon: bool = True

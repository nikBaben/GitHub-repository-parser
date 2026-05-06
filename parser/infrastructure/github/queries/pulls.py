from .base import (
    State, 
    Sort, 
    Direction,
    GitHubPaginatedQuery,
)


class PullsQuery(GitHubPaginatedQuery):
    """
    Модель запроса получения истории пуллов репозитория.
    """
    state: State
    sort: Sort
    direction: Direction

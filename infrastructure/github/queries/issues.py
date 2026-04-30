from .base import (
    State, 
    Sort,
    Direction,
    GitHubPaginatedQuery,
)


class IssuesQuery(GitHubPaginatedQuery):
    """"
    Модель запроса получения истории ишьюсов репозитория.
    """
    state: State
    sort: Sort
    direction: Direction

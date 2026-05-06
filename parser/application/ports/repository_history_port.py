from typing import Protocol
from datetime import datetime

from parser.domain.entities import (
    Repository,
    StarsHistory,
    ContributorsHistory,
    CommitsHistory, 
    ForksHistory,
    PullsHistory,
    MergedPullsHistory, 
    IssuesHistory,
)


class RepositoryHistoryPort(Protocol):
    """Порт для получения исторических данных репозитория"""
    async def get_repository(
        self,
        owner: str,
        repo: str,
    ) -> Repository:
        """Получает базовую информацию о репозитории."""
        ...

    async def get_forks_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> ForksHistory:
        """Получает историю форков репозитория."""
        ...

    async def get_pulls_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> PullsHistory:
        """Получает историю pull request'ов репозитория."""
        ...
    
    async def get_merged_pulls_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> MergedPullsHistory:
        """Получает историю смёрженных пуллов."""
        ...

    async def get_commits_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> CommitsHistory:
        """ Получает историю коммитов репозитория."""
        ...

    async def get_issues_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> IssuesHistory:
        ...
    
    async def get_contributors_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> ContributorsHistory:
        """Получает историю ишьюсов репозитория."""
        ...

    async def get_stars_history(
        self,
        owner: str, 
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> StarsHistory:
        """Получает историю контрибюторов репозитория."""
        ...



import asyncio
from datetime import datetime
from typing import cast

from application.dto import RepositoryHistoryDTO
from application.ports import RepositoryHistoryPort
from application.queries.queries import GetHistoryQuery
from domain.entities import (
    CommitsHistory,
    ContributorsHistory,
    ForksHistory,
    IssuesHistory,
    MergedPullsHistory,
    PullsHistory,
    Repository,
    StarsHistory,
)


class HistoryLoader:
    """Cервис для загрузки исторических данных репозитория."""
    def __init__(self, repository_history: RepositoryHistoryPort) -> None:
        self._repository_history = repository_history

    async def load(
        self,
        query: GetHistoryQuery,
        cutoff_dt: datetime | None,
    ) -> RepositoryHistoryDTO:
        """Загружает все исторические данные репозитория."""
        (
            repository,
            stars,
            forks,
            pulls,
            commits,
            merged_pulls,
            issues,
            contributors,
        ) = await asyncio.gather(
            self._repository_history.get_repository(query.owner, query.repo),
            self._repository_history.get_stars_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
            self._repository_history.get_forks_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
            self._repository_history.get_pulls_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
            self._repository_history.get_commits_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
            self._repository_history.get_merged_pulls_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
            self._repository_history.get_issues_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
            self._repository_history.get_contributors_history(
                query.owner,
                query.repo,
                cutoff_dt,
            ),
        )

        return RepositoryHistoryDTO(
            repository=cast(Repository, repository),
            stars=cast(StarsHistory, stars),
            forks=cast(ForksHistory, forks),
            pulls=cast(PullsHistory, pulls),
            commits=cast(CommitsHistory, commits),
            merged_pulls=cast(MergedPullsHistory, merged_pulls),
            issues=cast(IssuesHistory, issues),
            contributors=cast(ContributorsHistory, contributors),
        )

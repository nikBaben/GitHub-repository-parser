from datetime import datetime

from parser.domain.entities import (
    Repository, 
    StarsHistory, 
    ForksHistory, 
    PullsHistory, 
    CommitsHistory, 
    MergedPullsHistory,
    IssuesHistory,
    ContributorsHistory,
)
from parser.infrastructure.github.queries import (
    ForksQuery,
    PullsQuery,
    CommitsQuery,
    IssuesQuery,
    StarsQuery, 
    Sort,
    State,
    Direction,
    DatePriority,
)
from parser.infrastructure.github.clients.client import GitHubClient
from parser.infrastructure.github.mappers import (
    map_github_repository_to_domain,
    map_github_forks_to_domain,
    map_github_pulls_to_domain, 
    map_github_commits_to_domain,
    map_github_stars_to_domain,
    map_github_merged_pulls_to_domain,
    map_github_issues_to_domain,
    map_github_commits_to_contributors_history
)


class GitHubRepositoryHistoryAdapter:
    """Адаптер получения историчесческих данных репозитория GitHub."""
    def __init__(self, github_client: GitHubClient) -> None:
        self._github_client = github_client

    def stop_field_if_cutoff(
        self,
        cutoff_dt: datetime | None,
        field: DatePriority,
    ) -> DatePriority | None:
        """Возвращает поле для остановки пагинации, если задан cutoff_dt."""
        return field if cutoff_dt is not None else None

    async def get_repository(
        self,
        owner: str,
        repo: str,
    ) -> Repository:
        """Получает основне метрики репозитория из GitHub."""
        data, _ = await self._github_client.get_repository(owner, repo)
        return map_github_repository_to_domain(data)
    
    async def get_forks_history(
        self,
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> ForksHistory:
        """Получает историю форков репозитория из GitHub."""
        forks = await self._github_client.get_forks(
            owner, 
            repo, 
            ForksQuery(
                sort=Sort.NEWEST,
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.CREATED_AT),
            )
        )
        return map_github_forks_to_domain(
            owner=owner,
            repo=repo, 
            forks=forks
        )
    
    async def get_pulls_history(
        self,
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> PullsHistory:
        """Получает историю пулл реквестов репозитория из GitHub."""
        pulls = await self._github_client.get_pulls(
            owner,
            repo,
            PullsQuery(
                state=State.ALL,
                sort=Sort.CREATED,
                direction=Direction.DESC,
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.CREATED_AT),
            )
        ) 
        return map_github_pulls_to_domain(
            owner=owner, 
            repo=repo, 
            pulls=pulls
        )
    
    async def get_merged_pulls_history(
        self,
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> MergedPullsHistory:
        """Получает историю мерджет пулл реквестов из репозитория GitHub."""
        pulls = await self._github_client.get_pulls(
            owner,
            repo, 
            PullsQuery(
                state=State.CLOSED,
                sort=Sort.UPDATED,
                direction=Direction.DESC,
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.UPDATED_AT),
            )
        )
        return map_github_merged_pulls_to_domain(
            owner=owner,
            repo=repo,
            merged_pulls=pulls
        )

    async def get_commits_history(
        self,
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> CommitsHistory:
        """Получает историю коммитов из репозитория GitHub."""
        commits = await self._github_client.get_commits(
            owner,
            repo,
            CommitsQuery(
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.COMMIT_AUTHOR_DATE),
            )
        )
        return map_github_commits_to_domain(
            owner=owner,
            repo=repo,
            commits=commits
        )
    
    async def get_contributors_history(
        self,
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> ContributorsHistory:
        """
        Получает историю появления contributors на основе коммитов репозитория GitHub.

        GitHub Contributors API не отдаёт дату первого вклада, поэтому история
        контрибуторов строится по списку коммитов: для каждого автора берётся дата
        его самого раннего коммита в выбранном периоде.
        """
        commits = await self._github_client.get_commits(
            owner,
            repo,
            CommitsQuery(
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.COMMIT_AUTHOR_DATE),
            )
        )
        return map_github_commits_to_contributors_history(
            owner=owner,
            repo=repo,
            commits=commits
        )

    async def get_stars_history(
        self, 
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> StarsHistory:
        """Получает историю звезд из репозитория GitHub."""
        stars = await self._github_client.get_stars(
            owner, 
            repo, 
            StarsQuery(
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.STARRED_AT),
            )
        )
        return map_github_stars_to_domain(
            owner=owner,
            repo=repo,
            stars=stars
        )

    async def get_issues_history(
        self,
        owner: str,
        repo: str,
        cutoff_dt: datetime | None = None
    ) -> IssuesHistory:
        """Получает историю issues из репозитория GitHub."""
        issues = await self._github_client.get_issues(
            owner, 
            repo,  
            IssuesQuery(
                state=State.ALL,
                sort=Sort.CREATED,
                direction=Direction.DESC,
                cutoff_dt=cutoff_dt,
                stop_field=self.stop_field_if_cutoff(cutoff_dt, DatePriority.CREATED_AT),
            )
        )
        return map_github_issues_to_domain(
            owner=owner,
            repo=repo,
            issues=issues
        )
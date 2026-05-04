from domain.entities import (
    Repository,
    RepositoryMetrics,
    StarsHistory,
    PullsHistory,
    MergedPullsHistory,
    CommitsHistory,
    ForksHistory,
    IssuesHistory,
    ContributorsHistory,
)
from domain.value_objects import (
    Archived,
    Stars,
    Pulls,
    Commits,
    MergedPulls,
    Forks,
    Issues,
    Contributors,
    Watchers,
    OpenIssues,
    LastPush,
)


class CountMetricsService:
    """
    Доменный сервис для построения агрегированных количественных метрик репозитория.

    Отвечает за преобразование "сырых" исторических данных (history)
    и состояния репозитория (Repository) в набор доменных value objects,
    объединённых в модель RepositoryMetrics.
    """
    def build_count_metrics(
        self,
        repository: Repository,
        forks: ForksHistory,
        pulls: PullsHistory,
        commits: CommitsHistory,
        stars: StarsHistory,
        merged_pulls: MergedPullsHistory,
        issues:IssuesHistory,
        contributors:ContributorsHistory
    ) -> RepositoryMetrics:
        """
        Собирает агрегированные метрики репозитория на основе
        его состояния и исторических данных.
        """
        return RepositoryMetrics(
            archived=self._build_archived(repository),
            stars=self._count_stars(stars),
            pulls=self._count_pulls(pulls),
            commits=self._count_commits(commits),
            merged_pulls=self._count_merged_pulls(merged_pulls),
            forks=self._count_active_forks(forks),
            issues=self._count_issues(issues),
            contributors=self._count_contributors(contributors),
            watchers=self._count_watchers(repository),
            open_issues=self._build_open_issues(repository),
            last_push=self._build_last_push(repository),
        )

    def _build_archived(self, repository: Repository) -> Archived:
        """Собирает метрику архив."""
        return Archived(archived=repository.archived)

    def _count_stars(self, stars_history: StarsHistory) -> Stars:
        """Собирает метрику звезд."""
        return Stars(stars=len(stars_history.points))

    def _count_pulls(self, pulls_history: PullsHistory) -> Pulls:
        """Собирает метрику пуллов."""
        return Pulls(pulls=len(pulls_history.points))

    def _count_commits(self, commits_history: CommitsHistory) -> Commits:
        """Собирает метрику коммитов."""
        return Commits(commits=len(commits_history.points))

    def _count_merged_pulls(self, pulls_history: MergedPullsHistory) -> MergedPulls:
        """Собирает метрику мердж пуллов."""
        merged_count = sum(
            1
            for point in pulls_history.points
            if point.merged_at is not None
        )
        return MergedPulls(merged_pulls=merged_count)

    def _count_active_forks(self, forks_history: ForksHistory) -> Forks:
        """Собирает метрику форков."""
        forks_count = len(forks_history.points)
        return Forks(forks=forks_count)

    def _count_issues(self, issues_history: IssuesHistory) -> Issues:
        """Собирает метрику ишьюсов."""
        return Issues(issues=len(issues_history.points))

    def _count_contributors(
        self,
        contributors_history: ContributorsHistory,
    ) -> Contributors:
        """Собирает метрику контрибьюторов."""
        return Contributors(contributors=len(contributors_history.points))

    def _count_watchers(
        self,
        repository: Repository,
    ) -> Watchers:
        """Собирает метрику подписчков."""
        return Watchers(watchers=repository.watchers)

    def _build_open_issues(self, repository: Repository) -> OpenIssues:
        """Собирает метрику открытых ишьюсов."""
        return OpenIssues(open_issues=repository.open_issues)

    def _build_last_push(self, repository: Repository) -> LastPush:
        """Собирает метрику последнего пуша."""
        return LastPush(last_push=repository.pushed_at)

from pydantic import BaseModel

from domain.value_objects import (
    Archived,
    Commits,
    Contributors,
    Forks,
    Issues,
    OpenIssues,
    LastPush,
    Pulls,
    MergedPulls,
    Stars,
    Watchers,
)


class RepositoryMetrics(BaseModel):
    """
    Модель, представляющая агрегированные 
    количественные метрики репозитория
    """
    archived: Archived
    commits: Commits
    contributors: Contributors
    forks: Forks
    issues: Issues
    open_issues: OpenIssues
    last_push: LastPush
    pulls: Pulls
    merged_pulls: MergedPulls
    stars: Stars
    watchers: Watchers
from pydantic import BaseModel

from parser.domain.value_objects import (
    Archived,
    Commits,
    Contributors,
    Forks,
    Issues,
    OpenIssues,
    LastPush,
    MergedPulls,
    Pulls,
    Stars,
    Watchers,
    PopularityScore,
    ActivityScore,
    EngagementScore,
    DemandScore
)


class RepositoryScore(BaseModel):
    """Модель, представляющая полный скоринг репозитория"""
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
    popularity_score: PopularityScore
    activity_score: ActivityScore
    engagement_score: EngagementScore
    demand_score: DemandScore

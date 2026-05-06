from pydantic import BaseModel

from parser.domain.entities import Repository
from parser.domain.value_objects import (
    Archived,
    Stars,
    Forks, 
    Pulls, 
    Commits,
    MergedPulls,
    Issues,
    OpenIssues,
    LastPush,
    Contributors,
    Watchers,
    PopularityScore, 
    ActivityScore,
    EngagementScore,
    DemandScore
)


class RepositoryAnalyticsDTO(BaseModel):
    """DTO для передачи аналитических данных репозитория."""
    repository: Repository
    archived: Archived
    stars: Stars
    forks: Forks
    pulls: Pulls
    commits: Commits
    merged_pulls: MergedPulls
    issues: Issues
    open_issues: OpenIssues
    contributors: Contributors
    watchers: Watchers
    last_push: LastPush
    popularity_score: PopularityScore
    activity_score: ActivityScore
    engagement_score: EngagementScore
    demand_score: DemandScore

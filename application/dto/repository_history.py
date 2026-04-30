from pydantic import BaseModel

from domain.entities import (
    Repository,
    ForksHistory,
    PullsHistory,
    CommitsHistory, 
    StarsHistory,
    MergedPullsHistory,
    IssuesHistory,
    ContributorsHistory,
)


class RepositoryHistoryDTO(BaseModel):
    """DTO для передачи агрегированных исторических данных репозитория."""
    repository: Repository
    forks: ForksHistory
    pulls: PullsHistory
    commits: CommitsHistory
    stars: StarsHistory
    merged_pulls: MergedPullsHistory
    issues:IssuesHistory
    contributors:ContributorsHistory
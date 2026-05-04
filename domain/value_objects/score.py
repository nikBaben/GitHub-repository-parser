from pydantic import (
    BaseModel, 
    Field,
    field_validator
)
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


class PopularityScore(BaseModel):
    """Модель объекта-значения популярности репозитория."""
    popularity_score: float = Field(ge=0, le=100)

    @field_validator("popularity_score")
    @classmethod
    def round_popularity_score(cls, value: float) -> float:
        return round(value, 2)
    

class ActivityScore(BaseModel):
    """Модель объекта-значения активности репозитория."""
    activity_score: float = Field(ge=0, le=100)

    @field_validator("activity_score")
    @classmethod
    def round_activity_score(cls, value: float) -> float:
        return round(value, 2)
    

class EngagementScore(BaseModel):
    """Модель объекта-значения вовлеченности репозитория."""
    engagement_score: float = Field(ge=0, le=100)

    @field_validator("engagement_score")
    @classmethod
    def round_engagement_score(cls, value: float) -> float:
        return round(value, 2)
    

class DemandScore(BaseModel):
    """Модель объекта-значения спроса на репозиторий."""
    demand_score: float = Field(ge=0, le=100)

    @field_validator("demand_score")
    @classmethod
    def round_demand_score(cls, value: float) -> float:
        return round(value, 2)
    
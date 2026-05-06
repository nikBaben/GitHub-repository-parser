from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Pulls(BaseModel): 
    """Модель объекта-значения пуллов."""
    pulls: int = Field(ge=0)


class MergedPulls(BaseModel):
    """Модель объекта-значения мерджет пуллов."""
    merged_pulls: int = Field(ge=0)


class PullsHistoryPoint(BaseModel):
    """Модель объекта-значения истории пуллов."""
    pulled_at: datetime

    model_config = ConfigDict(frozen=True)


class MergedPullsHistoryPoint(BaseModel):
    """Модель объекта-значения истории мерджет пуллов."""
    merged_at: datetime

    model_config = ConfigDict(frozen=True)


from datetime import datetime

from pydantic import (
    BaseModel,
    Field, 
    ConfigDict
)


class Issues(BaseModel):
    """Модель объекта-значения ишьюсов."""
    issues: int = Field(ge=0) 


class OpenIssues(BaseModel):
    """Модель объекта-значения открытых ишьюсов."""
    open_issues: int = Field(ge=0) 


class IssuesHistoryPoint(BaseModel):
    """Модель объекта-значения истории ишьюсов."""
    issued_at: datetime

    model_config = ConfigDict(frozen=True)


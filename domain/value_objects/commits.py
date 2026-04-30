from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Commits(BaseModel):
    """Модель объекта-значения коммитов."""
    commits: int = Field(ge=0) 


class CommitsHistoryPoint(BaseModel):
    """Модель объекта-значения для истории коммитов."""
    committed_at: datetime
    
    model_config = ConfigDict(frozen=True)



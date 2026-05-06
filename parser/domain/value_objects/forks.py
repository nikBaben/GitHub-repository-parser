from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Forks(BaseModel):
    """Модель объекта-значения форков."""
    forks: int = Field(ge=0)  


class ForksHistoryPoint(BaseModel):
    """Модель объекта-значения истории форков."""
    forked_at: datetime

    model_config = ConfigDict(frozen=True)



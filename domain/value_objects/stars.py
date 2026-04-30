from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Stars(BaseModel): 
    """Модель объекта-значения звезд."""
    stars: int = Field(ge=0)


class StarsHistoryPoint(BaseModel):
    """Модель объекта-значения истории звезд."""
    starred_at: datetime

    model_config = ConfigDict(frozen=True)







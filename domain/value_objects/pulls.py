from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Pulls(BaseModel): 
    """Модель объекта-значения пуллов."""
    pulls: int = Field(ge=0)


class PullsHistoryPoint(BaseModel):
    """Модель объекта-значения для истории пуллов."""
    pulled_at: datetime

    model_config = ConfigDict(frozen=True)







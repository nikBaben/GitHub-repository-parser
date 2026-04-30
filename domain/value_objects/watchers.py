from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict, 
    Field
)


class Watchers(BaseModel):
    """Модель объекта-значения подписчиков."""
    watchers: int = Field(ge=0)


class WatchersHistoryPoint(BaseModel):
    """Модель объекта-значения истории подписчиков."""
    watched_at: datetime
    
    model_config = ConfigDict(frozen=True)




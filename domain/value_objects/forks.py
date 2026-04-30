from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict,
    Field
)


class Forks(BaseModel):
    forks: int = Field(ge=0)  


class ForksHistoryPoint(BaseModel):
    forked_at: datetime

    model_config = ConfigDict(frozen=True)



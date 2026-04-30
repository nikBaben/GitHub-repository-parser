from datetime import datetime

from pydantic import (
    BaseModel, 
    ConfigDict, 
    Field
)


class Contributors(BaseModel):
    """Модель объекта-значения контрибьюторов."""
    contributors: int = Field(ge=0) 


class ContributorsHistoryPoint(BaseModel):
    """Модель объекта-значения для истории контрибьюторов."""
    contirbuted_at: datetime
    
    model_config = ConfigDict(frozen=True)


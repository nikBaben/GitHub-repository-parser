from datetime import datetime

from pydantic import BaseModel


class LastPush(BaseModel):
    """Модель обекта-значения последнего пуша."""
    last_push: datetime





from datetime import datetime

from pydantic import BaseModel


class Repository(BaseModel):
    """Модель сущности репозитория."""
    name: str
    owner_login: str
    stars: int
    forks: int
    watchers: int
    open_issues: int
    archived: bool
    pushed_at: datetime 
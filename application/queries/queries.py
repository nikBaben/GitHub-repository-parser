from datetime import (
    datetime,
    timedelta, 
    timezone
)

from pydantic import BaseModel, computed_field

from infrastructure.github.utils import parse_github_url


class GetHistoryQuery(BaseModel):
    """Запрос получения исторических данных репозитория"""
    url: str
    days: int | None = None

    @computed_field
    @property
    def repo(self) -> str:
        """Название репозитория, извлечённое из URL."""
        _, repo = parse_github_url(self.url)
        return repo
    
    @computed_field
    @property
    def owner(self) -> str:
        """Владелец репозитория, извлечённый из URL."""
        owner, _ = parse_github_url(self.url)
        return owner

    @computed_field
    @property
    def cutoff_dt(self) -> datetime | None:
        """Дата отсечения истории."""
        if self.days is None:
            return None

        return datetime.now(timezone.utc) - timedelta(days=self.days)

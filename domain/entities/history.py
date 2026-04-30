from typing import Generic, TypeVar
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from value_objects import(
    CommitsHistoryPoint, 
    ContributorsHistoryPoint,
    ForksHistoryPoint,
    PullsHistoryPoint,
    MergedPullsHistoryPoint,
    IssuesHistoryPoint, 
    StarsHistoryPoint,
    WatchersHistoryPoint
)


Point = TypeVar("Point", bound=BaseModel)


class History(BaseModel, Generic[Point]):
    """
    Универсальная модель истории метрик репозитория.

    Представляет временной ряд значений (points) для конкретного репозитория,
    параметризованный типом точки (Point).

    Используется как обобщённая структура для всех видов исторических данных:
    звёзды, форки, коммиты и т.д.
    """
    owner: str
    repo: str
    points: list[Point]
    generated_at: datetime

    model_config = ConfigDict(frozen=True)


StarsHistory = History[StarsHistoryPoint]
"""Модель сущности истории изменения количества звёзд репозитория."""

WatchersHistory =  History[WatchersHistoryPoint]
"""Модель сущности истории изменения количества подписчиков репозитория."""

ContributorsHistory = History[ContributorsHistoryPoint]
"""Модель сущности истории изменения количества контрибюторов репозитория."""

CommitsHistory = History[CommitsHistoryPoint]
"""Модель сущности истории изменения количества коммитов репозитория."""

ForksHistory = History[ForksHistoryPoint]
"""Модель сущности истории изменения количества форков репозитория."""

PullsHistory = History[PullsHistoryPoint]
"""Модель сущности истории изменения количества пуллов репозитория."""

MergedPullsHistory = History[MergedPullsHistoryPoint]
"""Модель сущности истории изменения количества мерджет пуллов репозитория."""

IssuesHistory = History[IssuesHistoryPoint]
"""Модель сущности истории изменения количества ишьюсов репозитория."""

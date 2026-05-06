from datetime import datetime
from pydantic import BaseModel


class HistoryChartPoint(BaseModel):
    """
    Модель данных точки  для отображения на графике 
    истории метрик репозитория.
    """
    ts: datetime
    value: int


class HistoryChartModel(BaseModel):
    """
    Модель данных для отображения графика 
    истории метрик репозитория.
    """

    title: str
    x_title: str
    y_title: str
    points: list[HistoryChartPoint]
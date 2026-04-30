from datetime import datetime


def parse_dt(value: str | None = None) -> datetime | None:
    """Преобразует строковое представление даты/времени в объект datetime."""
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

from typing import Any
from datetime import datetime, timezone
from urllib.parse import urlparse


# Приоритет полей даты для разных типов GitHub сущностей
DATE_PRIORITY = [
    "starred_at",
    "created_at",
    "commit.author.date",
    "commit.committer.date",
    "updated_at",
    "pushed_at",
]


def parse_dt(value: str | None = None) -> datetime | None:
    """Преобразует строковое представление даты/времени в объект datetime."""
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def get_path(data: dict[str, Any], path: str) -> Any:
    """
    Извлекает значение из вложенного словаря по пути через точку.
    Позволяет безопасно получать вложенные значения без риска KeyError.
    """
    cur: Any = data
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def to_dt_utc(value: str | None) -> datetime | None:
    """Преобразует строку даты/времени в объект datetime в UTC."""
    if not value:
        return None
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc)


def to_iso_utc(value: str | None) -> str | None:
    """Преобразует строку даты/времени в ISO 8601 строку в UTC формате."""
    dt = to_dt_utc(value)
    if dt is None:
        return None
    return dt.isoformat().replace("+00:00", "Z")


def normalize_created_at(item: dict[str, Any]) -> dict[str, Any]:
    """
    Нормализует дату создания элемента из GitHub API.

    Пытается извлечь дату из различных возможных полей (в порядке приоритета),
    заданных в DATE_PRIORITY, и приводит её к унифицированному виду.
    """
    raw_date: str | None = None

    for path in DATE_PRIORITY:
        raw = get_path(item, path)
        if isinstance(raw, str) and raw:
            raw_date = raw
            break

    return {
        "created_at": to_iso_utc(raw_date),  # строка ISO
        "created_dt": to_dt_utc(raw_date),   # datetime объект
        "raw": item,
    }


def parse_github_url(url: str) -> tuple[str, str]:
    """Извлекает owner и repo из URL GitHub-репозитория."""
    if url.startswith("git@github.com:"):
        path = url.split("git@github.com:", 1)[1]
    else:
        parsed = urlparse(url)
        if parsed.netloc not in ("github.com", "www.github.com"):
            raise ValueError("Not github.com URL")
        path = parsed.path.lstrip("/")

    path = path.removesuffix(".git").strip("/")
    parts = path.split("/")

    if len(parts) < 2:
        raise ValueError("URL must contain owner/repo")

    return parts[0], parts[1]

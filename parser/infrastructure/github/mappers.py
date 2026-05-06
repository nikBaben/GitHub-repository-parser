from typing import Any, TypeVar
from collections.abc import Callable

from datetime import UTC, datetime

from parser.domain.entities import (
    Repository, 
    ForksHistory,
    PullsHistory, 
    CommitsHistory, 
    StarsHistory,
    MergedPullsHistory,  
    IssuesHistory,
    ContributorsHistory,
)
from parser.domain.value_objects import (
    ForksHistoryPoint,
    PullsHistoryPoint,
    CommitsHistoryPoint,
    StarsHistoryPoint,
    MergedPullsHistoryPoint,
    IssuesHistoryPoint, 
    ContributorsHistoryPoint
)
from .utils import parse_dt, normalize_created_at


TPoint = TypeVar("TPoint")
THistory = TypeVar("THistory")


def build_history(
    history_cls: type[THistory],
    owner: str,
    repo: str,
    points: list[TPoint],
) -> THistory:
    """
    Создаёт доменную сущность истории (History) из набора точек.

    Универсальный билдер для всех типов историй, устанавливает owner,
    repo, точки и время генерации.
    """
    return history_cls(
        owner=owner,
        repo=repo,
        points=points,
        generated_at=datetime.now(UTC),
    )


def build_history_points(
    items: list[dict[str, Any]],
    point_factory: Callable[[datetime], TPoint],
    sort_key: Callable[[TPoint], Any],
) -> list[TPoint]:
    """
    Преобразует список сырых данных GitHub API в список точек истории.

    Для каждого элемента извлекается дата создания, создаётся точка через
    point_factory и затем весь список сортируется.
    """
    points: list[TPoint] = []

    for item in items:
        created_dt = normalize_created_at(item)["created_dt"]
        if created_dt is None:
            continue

        points.append(point_factory(created_dt))

    points.sort(key=sort_key)
    return points


def map_github_repository_to_domain(data: dict[str, Any]) -> Repository:
    """Преобразует ответ GitHub API в доменную сущность Repository."""
    return Repository(
        name=data["name"],
        owner_login=data["owner"]["login"],
        stars=data["stargazers_count"],
        forks=data["forks_count"],
        watchers=data["subscribers_count"],
        open_issues=data["open_issues_count"],
        archived=data["archived"],
        pushed_at=parse_dt(data.get("pushed_at")),
    )


def map_github_forks_to_domain(
    owner: str,
    repo: str,
    forks: list[dict[str, Any]],
) -> ForksHistory:
    """Преобразует список форков GitHub API в историю форков."""
    points = build_history_points(
        items=forks,
        point_factory=lambda created_dt: ForksHistoryPoint(
            forked_at=created_dt,
        ),
        sort_key=lambda point: point.forked_at,
    )

    return build_history(
        history_cls=ForksHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def map_github_pulls_to_domain(
    owner: str,
    repo: str,
    pulls: list[dict[str, Any]],
) -> PullsHistory:
    """Преобразует список pull request'ов в историю PR."""
    points = build_history_points(
        items=pulls,
        point_factory=lambda created_dt: PullsHistoryPoint(
            pulled_at=created_dt,
        ),
        sort_key=lambda point: point.pulled_at,
    )

    return build_history(
        history_cls=PullsHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def map_github_commits_to_domain(
    owner: str,
    repo: str,
    commits: list[dict[str, Any]],
) -> CommitsHistory:
    """Преобразует список коммитов GitHub API в историю коммитов."""
    points = build_history_points(
        items=commits,
        point_factory=lambda created_dt: CommitsHistoryPoint(
            committed_at=created_dt,
        ),
        sort_key=lambda point: point.committed_at,
    )

    return build_history(
        history_cls=CommitsHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def map_github_stars_to_domain(
    owner: str,
    repo: str, 
    stars: list[dict[str, Any]],
) -> StarsHistory: 
    """Преобразует список звёзд GitHub API в историю stars."""
    points = build_history_points(
        items=stars,
        point_factory=lambda created_dt: StarsHistoryPoint(
            starred_at=created_dt,
        ),
        sort_key=lambda point: point.starred_at,
    )

    return build_history(
        history_cls=StarsHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def map_github_merged_pulls_to_domain(
    owner: str,
    repo: str, 
    merged_pulls: list[dict[str, Any]],
) -> MergedPullsHistory: 
    """
    Преобразует список pull request'ов в историю смёрженных PR.
    Учитывает только pull request'ы с заполненным полем merged_at.
    """
    points: list[MergedPullsHistoryPoint] = []
    for item in merged_pulls:
        merged_at_raw = item.get("merged_at")
        merged_at = parse_dt(merged_at_raw)
        if merged_at is None:
            continue
        points.append(MergedPullsHistoryPoint(merged_at=merged_at))

    points.sort(key=lambda point: point.merged_at)

    return build_history(
        history_cls=MergedPullsHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def map_github_issues_to_domain(
    owner: str,
    repo: str, 
    issues: list[dict[str, Any]],
) -> IssuesHistory: 
    """
    Преобразует список issues GitHub API в историю issues.
    Исключает элементы, являющиеся pull request'ами.
    """
    pure_issues = [
        item
        for item in issues
        if "pull_request" not in item
    ]

    points = build_history_points(
        items=pure_issues,
        point_factory=lambda created_dt: IssuesHistoryPoint(
            issued_at=created_dt,
        ),
        sort_key=lambda point: point.issued_at,
    )

    return build_history(
        history_cls=IssuesHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def map_github_contributors_to_domain(
    owner: str,
    repo: str, 
    stars: list[dict[str, Any]],
) -> ContributorsHistory: 
    """
    Преобразует список данных в историю contributors.
    Использует даты событий для формирования точек истории.
    """
    points = build_history_points(
        items=stars,
        point_factory=lambda created_dt: ContributorsHistoryPoint(
            contirbuted_at=created_dt,
        ),
        sort_key=lambda point: point.contirbuted_at,
    )

    return build_history(
        history_cls=ContributorsHistory,
        owner=owner,
        repo=repo,
        points=points,
    )


def _author_key(commit: dict[str, Any]) -> str | None:
    """Формирует уникальный идентификатор автора коммита."""
    author = commit.get("author") or {}
    if isinstance(author, dict) and author.get("login"):
        return f"login:{author['login']}"

    commit_author = (commit.get("commit") or {}).get("author") or {}
    email = commit_author.get("email")
    name = commit_author.get("name")
    if email:
        return f"email:{email.lower()}"
    if name:
        return f"name:{name.lower()}"
    return None


def map_github_commits_to_contributors_history(
    owner: str,
    repo: str,
    commits: list[dict[str, Any]],
) -> ContributorsHistory:
    """
    Строит историю появления contributors на основе коммитов.

    Для каждого автора определяется дата его первого коммита,
    после чего формируется история появления участников.
    """
    # ключ -> дата самого раннего вклада
    first_seen_by_author: dict[str, datetime] = {}

    for item in commits:
        created_dt = normalize_created_at(item)["created_dt"]
        if created_dt is None:
            continue

        key = _author_key(item)
        if key is None:
            continue

        prev = first_seen_by_author.get(key)
        if prev is None or created_dt < prev:
            first_seen_by_author[key] = created_dt

    points = [
        ContributorsHistoryPoint(contirbuted_at=dt)
        for dt in sorted(first_seen_by_author.values())
    ]

    return ContributorsHistory(
        owner=owner,
        repo=repo,
        points=points,
        generated_at=datetime.now(UTC),
    )

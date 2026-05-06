from typing import Literal
from collections import Counter

from datetime import (
    datetime, 
    timedelta, 
    timezone
)

from parser.application.dto import RepositoryHistoryDTO
from parser.presentation.chart.line_chart import (
    HistoryChartModel,
    HistoryChartPoint,
)


BucketType = Literal["day", "week", "month"]


class HistoryChartMapper:
    """Маппер исторических данных репозитория в модели графиков."""
    @staticmethod
    def _bucket_key(ts: datetime, bucket: BucketType) -> datetime:
        """Возвращает начало временного интервала для указанной даты."""
        ts = ts.astimezone(timezone.utc)

        if bucket == "day":
            return datetime(ts.year, ts.month, ts.day, tzinfo=timezone.utc)

        if bucket == "week":
            monday = ts - timedelta(days=ts.weekday())
            return datetime(monday.year, monday.month, monday.day, tzinfo=timezone.utc)

        if bucket == "month":
            return datetime(ts.year, ts.month, 1, tzinfo=timezone.utc)

        raise ValueError("bucket must be: 'day', 'week', or 'month'")

    @classmethod
    def _build_chart_from_datetimes(
        cls,
        datetimes: list[datetime],
        title: str,
        x_title: str,
        y_title: str,
        bucket: BucketType,
    ) -> HistoryChartModel:
        """Создаёт модель исторического графика из списка дат событий."""
        if not datetimes:
            return HistoryChartModel(
                title=title,
                x_title=x_title,
                y_title=y_title,
                points=[],
            )

        grouped_keys = [cls._bucket_key(dt, bucket) for dt in datetimes]
        counts = Counter(grouped_keys)

        sorted_x = sorted(counts.keys())

        points = [
            HistoryChartPoint(ts=dt, value=counts[dt])
            for dt in sorted_x
        ]

        return HistoryChartModel(
            title=title,
            x_title=x_title,
            y_title=y_title,
            points=points,
        )

    @classmethod
    def to_forks_chart(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории форков репозитория."""
        datetimes = sorted(
            [point.forked_at for point in history.forks.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Forks history: {history.forks.owner}/{history.forks.repo}",
            x_title="Period start (UTC)",
            y_title="Forks count",
            bucket=bucket,
        )

    @classmethod
    def to_pulls_chart(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории pull request'ов репозитория."""
        datetimes = sorted(
            [point.pulled_at for point in history.pulls.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Pull requests history: {history.pulls.owner}/{history.pulls.repo}",
            x_title="Period start (UTC)",
            y_title="Pull requests count",
            bucket=bucket,
        )

    @classmethod
    def to_commits_chart(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории коммитов репозитория."""
        datetimes = sorted(
            [point.committed_at for point in history.commits.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Commits history: {history.commits.owner}/{history.commits.repo}",
            x_title="Period start (UTC)",
            y_title="Commits count",
            bucket=bucket,
        )
    
    @classmethod
    def to_stars_chart(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории звёзд репозитория."""
        datetimes = sorted(
            [point.starred_at for point in history.stars.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Stars history: {history.stars.owner}/{history.stars.repo}",
            x_title="Period start (UTC)",
            y_title="Stars count",
            bucket=bucket,
        )
    
    @classmethod
    def to_merged_pulls_chart(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории смерженных pull request'ов репозитория."""
        datetimes = sorted(
            [point.merged_at for point in history.merged_pulls.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Merged pulls history: {history.merged_pulls.owner}/{history.merged_pulls.repo}",
            x_title="Period start (UTC)",
            y_title="Merged pulls count",
            bucket=bucket,
        )
    
    @classmethod
    def to_issues_chart(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории ишьюсов репозитория."""
        datetimes = sorted(
            [point.issued_at for point in history.issues.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Issues history: {history.issues.owner}/{history.issues.repo}",
            x_title="Period start (UTC)",
            y_title="Issues count",
            bucket=bucket,
        )
    
    @classmethod
    def to_contributors_charts(
        cls,
        history: RepositoryHistoryDTO,
        bucket: BucketType = "week",
    ) -> HistoryChartModel:
        """Создаёт график истории контрибьюторов репозитория."""
        datetimes = sorted(
            [point.contirbuted_at for point in history.contributors.points]
        )

        return cls._build_chart_from_datetimes(
            datetimes=datetimes,
            title=f"Contributors history: {history.contributors.owner}/{history.contributors.repo}",
            x_title="Period start (UTC)",
            y_title="Contributors count",
            bucket=bucket,
        )




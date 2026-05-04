from math import isclose

from pydantic import(
    BaseModel,
    ConfigDict,
    Field,
    model_validator
)

from domain.entities import RepositoryMetrics, RepositoryScore
from domain.value_objects import (
    PopularityScore,
    ActivityScore,
    EngagementScore,
    DemandScore,
)
from domain.utils import (
    to_score_100,
    log_ratio,
    linear_ratio,
)


class ScoreConfig(BaseModel):
    """
    Конфигурация весов
    и порогов насыщения 
    для расчёта оценки репозитория.
    """
    model_config = ConfigDict(frozen=True)

    stars_saturation: int = Field(gt=0)
    forks_saturation: int = Field(gt=0)
    contributors_saturation: int = Field(gt=0)
    merged_pulls_saturation: int = Field(gt=0)
    commits_saturation: int = Field(gt=0)
    issues_saturation: int = Field(gt=0)

    popularity_stars_weight: float = 0.70
    popularity_forks_weight: float = 0.30

    activity_contributors_weight: float = 0.35
    activity_merged_pulls_weight: float = 0.35
    activity_commits_weight: float = 0.30

    engagement_forks_weight: float = 0.50
    engagement_issues_weight: float = 0.50

    demand_popularity_weight: float = 0.45
    demand_activity_weight: float = 0.40
    demand_engagement_weight: float = 0.15

    @model_validator(mode="after")
    def validate_weight_groups(self) -> "ScoreConfig":
        """Проверяет корректность весов во всех группах."""
        self._validate_weight_sum(
            group_name="popularity",
            weights=[
                self.popularity_stars_weight,
                self.popularity_forks_weight,
            ],
        )
        self._validate_weight_sum(
            group_name="activity",
            weights=[
                self.activity_contributors_weight,
                self.activity_merged_pulls_weight,
                self.activity_commits_weight,
            ],
        )
        self._validate_weight_sum(
            group_name="engagement",
            weights=[
                self.engagement_forks_weight,
                self.engagement_issues_weight,
            ],
        )
        self._validate_weight_sum(
            group_name="demand",
            weights=[
                self.demand_popularity_weight,
                self.demand_activity_weight,
                self.demand_engagement_weight,
            ],
        )

        return self

    @staticmethod
    def _validate_weight_sum(
        group_name: str,
        weights: list[float],
    ) -> None:
        """Проверяет, что сумма весов в группе равна 1.0."""
        if not isclose(sum(weights), 1.0):
            raise ValueError(f"{group_name} weights must sum to 1.0")


class RepositoryScoringService:
    """Доменный сервис для расчёта скоринга репозитория."""
    def __init__(self, config: ScoreConfig) -> None:
        self._config = config

    def calculate(self, metrics: RepositoryMetrics) -> RepositoryScore:
        """Выполняет полный расчёт скоринга репозитория."""
        popularity_score = self._calculate_popularity_score(metrics)
        activity_score = self._calculate_activity_score(metrics)
        engagement_score = self._calculate_engagement_score(metrics)

        demand_score = self._calculate_demand_score(
            popularity_score=popularity_score,
            activity_score=activity_score,
            engagement_score=engagement_score,
        )

        return RepositoryScore(
            **metrics.model_dump(),
            popularity_score=PopularityScore(
                popularity_score=popularity_score,
            ),
            activity_score=ActivityScore(
                activity_score=activity_score,
            ),
            engagement_score=EngagementScore(
                engagement_score=engagement_score,
            ),
            demand_score=DemandScore(
                demand_score=demand_score,
            ),
        )

    def _calculate_popularity_score(
        self,
        metrics: RepositoryMetrics,
    ) -> float:
        """
        Рассчитывает популярность репозитория.
        Используемые метрики:
            - stars (логарифмическая нормализация)
            - forks (логарифмическая нормализация)
        """
        stars_ratio = log_ratio(
            metrics.stars.stars,
            self._config.stars_saturation,
        )
        forks_ratio = log_ratio(
            metrics.forks.forks,
            self._config.forks_saturation,
        )

        popularity_ratio = (
            stars_ratio * self._config.popularity_stars_weight
            + forks_ratio * self._config.popularity_forks_weight
        )

        return to_score_100(popularity_ratio)

    def _calculate_activity_score(
        self,
        metrics: RepositoryMetrics,
    ) -> float:
        """
        Рассчитывает активность репозитория.
        Используемые метрики:
            - contributors (линейная нормализация)
            - merged_pulls (логарифмическая нормализация)
            - commits (логарифмическая нормализация)
        """
        contributors_ratio = linear_ratio(
            metrics.contributors.contributors,
            self._config.contributors_saturation,
        )
        merged_pulls_ratio = log_ratio(
            metrics.merged_pulls.merged_pulls,
            self._config.merged_pulls_saturation,
        )
        commits_ratio = log_ratio(
            metrics.commits.commits,
            self._config.commits_saturation,
        )

        activity_ratio = (
            contributors_ratio * self._config.activity_contributors_weight
            + merged_pulls_ratio * self._config.activity_merged_pulls_weight
            + commits_ratio * self._config.activity_commits_weight
        )

        return to_score_100(activity_ratio)

    def _calculate_engagement_score(
        self,
        metrics: RepositoryMetrics,
    ) -> float:
        """
        Рассчитывает вовлечённость пользователей.
        Используемые метрики:
            - forks (логарифмическая нормализация)
            - issues (логарифмическая нормализация)
        """
        
        forks_ratio = log_ratio(
            metrics.forks.forks,
            self._config.forks_saturation,
        )
        issues_ratio = log_ratio(
            metrics.issues.issues,
            self._config.issues_saturation,
        )

        engagement_ratio = (
            forks_ratio * self._config.engagement_forks_weight
            + issues_ratio * self._config.engagement_issues_weight
        )

        return to_score_100(engagement_ratio)

    def _calculate_demand_score(
        self,
        popularity_score: float,
        activity_score: float,
        engagement_score: float,
    ) -> float:
        """Рассчитывает итоговый спрос."""
        demand_score = (
            popularity_score * self._config.demand_popularity_weight
            + activity_score * self._config.demand_activity_weight
            + engagement_score * self._config.demand_engagement_weight
        )

        return round(demand_score, 2)

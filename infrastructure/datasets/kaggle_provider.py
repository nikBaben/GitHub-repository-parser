from pathlib import Path
import numpy as np
import pandas as pd

from domain.services import ScoreConfig


class KaggleScoreConfigProvider:
    """Провайдер конфигурации скоринга на основе датасета Kaggle."""
    def __init__(
        self,
        csv_path: str | Path,
        percentile: float = 0.99,
    ) -> None:
        if not 0 < percentile <= 1:
            raise ValueError("percentile must be in range (0, 1]")

        self._csv_path = Path(csv_path)
        self._percentile = percentile

    def get_config(self) -> ScoreConfig:
        """Строит и возвращает конфигурацию скоринга."""
        df = pd.read_csv(self._csv_path)
        self._validate_columns(df)

        df = df[df["is_archived"] == 0]
        df = df[df["is_fork"] == 0]

        metrics = self._build_metric_series(df)
        saturations = {
            "stars_saturation": self._percentile_value(metrics["stars"]),
            "forks_saturation": self._percentile_value(metrics["forks"]),
            "contributors_saturation": self._percentile_value(metrics["contributors"]),
            "merged_pulls_saturation": self._percentile_value(
                metrics["merged_pulls"],
            ),
            "commits_saturation": self._percentile_value(metrics["commits"]),
            "issues_saturation": self._percentile_value(metrics["issues"]),
        }
        weights = self._build_score_weights(
            metrics=metrics,
            saturations=saturations,
        )

        return ScoreConfig(
            **saturations,
            popularity_stars_weight=weights["popularity"]["stars"],
            popularity_forks_weight=weights["popularity"]["forks"],
            activity_contributors_weight=weights["activity"]["contributors"],
            activity_merged_pulls_weight=weights["activity"]["merged_pulls"],
            activity_commits_weight=weights["activity"]["commits"],
            engagement_forks_weight=weights["engagement"]["forks"],
            engagement_issues_weight=weights["engagement"]["issues"],
            demand_popularity_weight=weights["demand"]["popularity"],
            demand_activity_weight=weights["demand"]["activity"],
            demand_engagement_weight=weights["demand"]["engagement"],
        )

    def _build_metric_series(self, df: pd.DataFrame) -> dict[str, pd.Series]:
        """Формирует словарь числовых рядов метрик из DataFrame."""
        open_issues = self._numeric_series(df["open_issues"])
        closed_issues = self._numeric_series(df["closed_issues"])

        return {
            "stars": self._numeric_series(df["stars"]),
            "forks": self._numeric_series(df["forks"]),
            "contributors": self._numeric_series(df["contributors"]),
            "merged_pulls": self._numeric_series(df["merged_pull_requests"]),
            "commits": self._numeric_series(df["commits"]),
            "issues": open_issues + closed_issues,
        }

    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Проверяет наличие необходимых колонок в датасете."""
        required_columns = {
            "stars",
            "forks",
            "contributors",
            "merged_pull_requests",
            "commits",
            "open_issues",
            "closed_issues",
            "is_archived",
            "is_fork",
        }
        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Kaggle dataset is missing columns: {missing}")

    def _numeric_series(self, series: pd.Series) -> pd.Series:
        """Приводит серию к числовому типу и очищает данные."""
        return pd.to_numeric(series, errors="coerce").fillna(0).clip(lower=0)

    def _percentile_value(self, series: pd.Series) -> int:
        """Вычисляет значение saturation на основе percentile."""
        value = self._numeric_series(series).quantile(self._percentile)

        return max(int(round(value)), 1)

    def _build_score_weights(
        self,
        metrics: dict[str, pd.Series],
        saturations: dict[str, int],
    ) -> dict[str, dict[str, float]]:
        """Вычисляет веса для всех групп скоринга."""
        ratios = self._build_metric_ratios(
            metrics=metrics,
            saturations=saturations,
        )
        target = ratios.mean(axis=1)

        popularity_weights = self._weights_from_correlations(
            features={
                "stars": ratios["stars"],
                "forks": ratios["forks"],
            },
            target=target,
        )
        activity_weights = self._weights_from_correlations(
            features={
                "contributors": ratios["contributors"],
                "merged_pulls": ratios["merged_pulls"],
                "commits": ratios["commits"],
            },
            target=target,
        )
        engagement_weights = self._weights_from_correlations(
            features={
                "forks": ratios["forks"],
                "issues": ratios["issues"],
            },
            target=target,
        )

        category_ratios = {
            "popularity": (
                ratios["stars"] * popularity_weights["stars"]
                + ratios["forks"] * popularity_weights["forks"]
            ),
            "activity": (
                ratios["contributors"] * activity_weights["contributors"]
                + ratios["merged_pulls"] * activity_weights["merged_pulls"]
                + ratios["commits"] * activity_weights["commits"]
            ),
            "engagement": (
                ratios["forks"] * engagement_weights["forks"]
                + ratios["issues"] * engagement_weights["issues"]
            ),
        }
        demand_weights = self._weights_from_correlations(
            features=category_ratios,
            target=target,
        )

        return {
            "popularity": popularity_weights,
            "activity": activity_weights,
            "engagement": engagement_weights,
            "demand": demand_weights,
        }

    def _build_metric_ratios(
        self,
        metrics: dict[str, pd.Series],
        saturations: dict[str, int],
    ) -> pd.DataFrame:
        """Строит DataFrame нормализованных метрик (0..1)."""
        return pd.DataFrame(
            {
                "stars": self._log_ratio_series(
                    metrics["stars"],
                    saturations["stars_saturation"],
                ),
                "forks": self._log_ratio_series(
                    metrics["forks"],
                    saturations["forks_saturation"],
                ),
                "contributors": self._linear_ratio_series(
                    metrics["contributors"],
                    saturations["contributors_saturation"],
                ),
                "merged_pulls": self._log_ratio_series(
                    metrics["merged_pulls"],
                    saturations["merged_pulls_saturation"],
                ),
                "commits": self._log_ratio_series(
                    metrics["commits"],
                    saturations["commits_saturation"],
                ),
                "issues": self._log_ratio_series(
                    metrics["issues"],
                    saturations["issues_saturation"],
                ),
            }
        )

    def _linear_ratio_series(
        self,
        series: pd.Series,
        saturation: int,
    ) -> pd.Series:
        """Линейная нормализация серии в диапазон (0..1)."""
        return (self._numeric_series(series) / saturation).clip(lower=0, upper=1)

    def _log_ratio_series(
        self,
        series: pd.Series,
        saturation: int,
    ) -> pd.Series:
        """Логарифмическая нормализация серии (для heavy-tail распределений)."""
        values = np.log1p(self._numeric_series(series))
        saturation_value = np.log1p(saturation)

        return (values / saturation_value).clip(lower=0, upper=1)

    def _weights_from_correlations(
        self,
        features: dict[str, pd.Series],
        target: pd.Series,
    ) -> dict[str, float]:
        """Вычисляет веса признаков на основе корреляции с target."""
        scores: dict[str, float] = {}

        for name, series in features.items():
            correlation = series.corr(target, method="spearman")

            if pd.isna(correlation):
                scores[name] = 0.0
            else:
                scores[name] = max(float(correlation), 0.0)

        return self._normalize_weights(scores)

    def _normalize_weights(self, scores: dict[str, float]) -> dict[str, float]:
        """Нормализует веса так, чтобы их сумма была равна 1.0."""
        if not scores:
            raise ValueError("scores must not be empty")

        total = sum(scores.values())

        if total <= 0:
            equal_weight = 1.0 / len(scores)
            return self._normalize_last_weight(
                {name: equal_weight for name in scores}
            )

        return self._normalize_last_weight(
            {
                name: score / total
                for name, score in scores.items()
            }
        )

    def _normalize_last_weight(
        self,
        weights: dict[str, float],
    ) -> dict[str, float]:
        """Корректирует последний вес для точного соблюдения суммы = 1.0."""
        names = list(weights)

        if len(names) == 1:
            return {names[0]: 1.0}

        normalized = {
            name: weights[name]
            for name in names[:-1]
        }
        normalized[names[-1]] = 1.0 - sum(normalized.values())

        return normalized

import math


def clamp_non_negative(value: int | float) -> float:
    """Не допускает отрицательных значений в вычислениях."""
    return max(float(value), 0.0)


def clamp_ratio(value: float) -> float:
    """Ограничивает ratio диапазоном 0..1."""
    return min(max(value, 0.0), 1.0)


def linear_ratio(value: int | float, saturation_point: int | float) -> float:
    """Линейная нормализация в диапазон 0..1."""
    if saturation_point <= 0:
        raise ValueError("saturation_point must be greater than 0")

    value = clamp_non_negative(value)

    if value == 0:
        return 0.0

    return clamp_ratio(value / saturation_point)


def log_ratio(value: int | float, saturation_point: int | float) -> float:
    """
    Логарифмическая нормализация в диапазон 0..1.

    Подходит для heavy-tail метрик:
    - stars
    - forks
    - merged PRs
    - commits
    - issues
    """
    if saturation_point <= 0:
        raise ValueError("saturation_point must be greater than 0")

    value = clamp_non_negative(value)

    if value == 0:
        return 0.0

    return clamp_ratio(math.log1p(value) / math.log1p(saturation_point))


def to_score_100(value: float) -> float:
    """Переводит значение 0..1 в диапазон 0..100."""
    return round(clamp_ratio(value) * 100, 2)

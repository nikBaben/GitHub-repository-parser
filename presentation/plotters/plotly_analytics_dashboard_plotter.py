from typing import Any

import plotly.graph_objects as go

from presentation.chart.line_chart import HistoryChartModel
from presentation.view_models import (
    RepositoryAnalyticsViewModel,
    RepositoryDashboardViewModel,
    RepositorySummaryViewModel
)


class PlotlyAnalyticsDashboardPlotter:
    """Построитель интерактивного Plotly-дашборда аналитики репозитория."""
    CHART_X_DOMAIN = [0.0, 0.79]
    CHART_Y_DOMAIN = [0.0, 0.98]
    CHART_TITLE_X = 0.395
    SIDEBAR_X0 = 0.825
    SIDEBAR_CONTENT_X = 0.845
    SIDEBAR_BUTTON_Y = 0.36

    @staticmethod
    def _cumulative_values(chart: HistoryChartModel) -> list[int]:
        """Возвращает накопительные значения для точек исторического графика."""
        total = 0
        values: list[int] = []

        for point in chart.points:
            total += point.value
            values.append(total)

        return values

    @staticmethod
    def _visibility_pair(
        metric_index: int,
        metrics_count: int,
    ) -> list[bool]:
        """
        Формирует список видимости traces для выбранной метрики.

        Для каждой метрики используется две линии: 
        значение за период и накопительное значение.
        """
        visible = [False] * (metrics_count * 2)
        visible[metric_index * 2] = True
        visible[metric_index * 2 + 1] = True
        return visible

    @staticmethod
    def _axis_dtick(values: list[int]) -> int | None:
        """
        Возвращает шаг делений оси Y 
        для небольших целочисленных значений.
        """
        if not values:
            return 1

        return 1 if max(values) < 20 else None

    @classmethod
    def _chart_axis_updates(
        cls,
        chart: HistoryChartModel,
    ) -> dict[str, dict[str, Any]]:
        """Формирует обновления осей графика для выбранной метрики."""
        per_period_values = [point.value for point in chart.points]
        cumulative_values = cls._cumulative_values(chart)

        return {
            "yaxis": {
                "title": {"text": "Count per period", "standoff": 12},
                "domain": cls.CHART_Y_DOMAIN,
                "rangemode": "tozero",
                "autorange": True,
                "visible": True,
                "showgrid": True,
                "showticklabels": True,
                "automargin": False,
                "tick0": 0,
                "tickformat": "d",
                "dtick": cls._axis_dtick(per_period_values),
            },
            "yaxis2": {
                "title": {"text": "Cumulative", "standoff": 4},
                "overlaying": "y",
                "side": "right",
                "rangemode": "tozero",
                "autorange": True,
                "visible": True,
                "showgrid": False,
                "showticklabels": True,
                "automargin": False,
                "tick0": 0,
                "tickformat": "d",
                "dtick": cls._axis_dtick(cumulative_values),
            },
        }

    @classmethod
    def _add_history_traces(
        cls,
        figure: go.Figure,
        chart: HistoryChartModel,
        name: str,
        visible: bool,
    ) -> None:
        """
        Добавляет на фигуру линии значений
        за период и накопительных значений.
        """
        x_values = [point.ts for point in chart.points]
        y_values = [point.value for point in chart.points]

        figure.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                name=f"{name} per period",
                visible=visible,
                hovertemplate=(
                    "Period start: %{x|%Y-%m-%d}<br>"
                    f"{name}: " + "%{y}<extra></extra>"
                ),
            )
        )
        figure.add_trace(
            go.Scatter(
                x=x_values,
                y=cls._cumulative_values(chart),
                mode="lines+markers",
                name=f"{name} cumulative",
                visible=visible,
                yaxis="y2",
                line={"dash": "dash"},
                hovertemplate=(
                    "Period start: %{x|%Y-%m-%d}<br>"
                    f"{name} cumulative: " + "%{y}<extra></extra>"
                ),
            )
        )

    @staticmethod
    def _build_summary_text(summary: RepositorySummaryViewModel) -> str:
        """Формирует HTML-текст со сводной информацией о репозитории."""
        return (
            f"<b>{summary.full_name}</b><br>"
            f"Stars: {summary.stars}<br>"
            f"Watchers: {summary.watchers}<br>"
            f"Open issues: {summary.open_issues}<br>"
            f"Archived: {'Yes' if summary.archived else 'No'}<br>"
            f"Total forks: {summary.total_forks}<br>"
            f"Total pulls: {summary.total_pulls}<br>"
            f"Total commits: {summary.total_commits}"
        )

    @staticmethod
    def _build_analytics_text(analytics: RepositoryAnalyticsViewModel) -> str:
        """Формирует HTML-текст с аналитическими показателями репозитория."""
        return (
            "<b>Analytics</b><br>"
            f"Stars metric: {analytics.stars_metric}<br>"
            f"Active forks: {analytics.active_forks}<br>"
            f"Pulls metric: {analytics.pulls_metric}<br>"
            f"Commits metric: {analytics.commits_metric}<br>"
            f"Merged pulls: {analytics.merged_pulls}<br>"
            f"Issues metric: {analytics.issues_metric}<br>"
            f"Contributors: {analytics.contributors}<br>"
            f"Popularity: {analytics.popularity}<br>"
            f"Activity: {analytics.activity}<br>"
            f"Engagement: {analytics.engagement}<br>"
            f"Demand: {analytics.demand}"
        )

    @classmethod
    def build_figure(
        cls,
        dashboard: RepositoryDashboardViewModel,
    ) -> go.Figure:
        """Создаёт Plotly-фигуру с графиками, сводкой и аналитикой репозитория."""
        summary_text = cls._build_summary_text(dashboard.summary)
        analytics_text = cls._build_analytics_text(dashboard.analytics)
        summary_annotation = {
            "width": 220,
            "xref": "paper",
            "yref": "paper",
            "x": cls.SIDEBAR_CONTENT_X,
            "y": 1.0,
            "xanchor": "left",
            "yanchor": "top",
            "align": "left",
            "showarrow": False,
            "text": summary_text,
            "bordercolor": "#D9D9D9",
            "borderwidth": 1,
            "borderpad": 8,
            "bgcolor": "#F9F9F9",
        }
        analytics_annotation = {
            "width": 220,
            "align": "left",
            "xref": "paper",
            "yref": "paper",
            "x": cls.SIDEBAR_CONTENT_X,
            "y": 0.725,
            "xanchor": "left",
            "yanchor": "top",
            "align": "left",
            "showarrow": False,
            "text": analytics_text,
            "bordercolor": "#D9D9D9",
            "borderwidth": 1,
            "borderpad": 8,
            "bgcolor": "#F9F9F9",
        }

        figure = go.Figure()

        metrics = dashboard.metrics

        for index, metric in enumerate(metrics):
            cls._add_history_traces(
                figure=figure,
                chart=metric.chart,
                name=metric.name,
                visible=index == 0,
        )

        initial_title = metrics[0].title if metrics else "Repository history"
        initial_chart = metrics[0].chart if metrics else HistoryChartModel(
            title="Repository history",
            x_title="Period start (UTC)",
            y_title="Count per period",
            points=[],
        )

        figure.update_layout(
            autosize=True,
            title={
                "text": initial_title,
                "x": cls.CHART_TITLE_X,
                "xanchor": "center",
            },
            xaxis={
                "title": {"text": "Period start (UTC)", "standoff": 16},
                "domain": cls.CHART_X_DOMAIN,
                "automargin": False,
                "fixedrange": True,
            },
            yaxis={
                "title": {"text": "Count per period", "standoff": 12},
                "domain": cls.CHART_Y_DOMAIN,
                "rangemode": "tozero",
                "automargin": False,
                "visible": True,
                "showticklabels": True,
                "fixedrange": True,
                "tick0": 0,
                "tickformat": "d",
            },
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#F7F9FC",
            yaxis2={
                "title": {"text": "Cumulative", "standoff": 4},
                "overlaying": "y",
                "side": "right",
                "rangemode": "tozero",
                "showgrid": False,
                "automargin": False,
                "fixedrange": True,
                "tick0": 0,
                "tickformat": "d",
            },
            template="plotly_white",
            hovermode="x unified",
            uirevision="static-dashboard-layout",
            transition={"duration": 0},
            showlegend=True,
            legend={
                "title": {"text": "Charts"},
                "orientation": "h",
                "x": 0,
                "y": 1.08,
                "xanchor": "left",
                "yanchor": "bottom",
            },
            margin={"l": 90, "r": 40, "t": 110, "b": 90},
            shapes=[
                {
                    "type": "rect",
                    "xref": "paper",
                    "yref": "paper",
                    "x0": cls.SIDEBAR_X0,
                    "x1": 1.06,
                    "y0": -0.16,
                    "y1": 1.16,
                    "fillcolor": "#F1F5F9",
                    "line": {"width": 0},
                    "layer": "below",
                },
            ],
            annotations=[summary_annotation, analytics_annotation],
            updatemenus=[
                {
                    "type": "buttons",
                    "direction": "down",
                    "x": cls.SIDEBAR_CONTENT_X,
                    "y": cls.SIDEBAR_BUTTON_Y,
                    "xanchor": "left",
                    "yanchor": "top",
                    "showactive": True,
                    "buttons": [
                        *[
                            {
                                "label": metric.name,
                                "method": "update",
                                "args": [
                                    {
                                        "visible": cls._visibility_pair(
                                            metric_index=index,
                                            metrics_count=len(metrics),
                                        )
                                    },
                                    {
                                        "title": {
                                            "text": metric.title,
                                            "x": cls.CHART_TITLE_X,
                                            "xanchor": "center",
                                        },
                                        "annotations": [summary_annotation, analytics_annotation],
                                        **cls._chart_axis_updates(metric.chart),
                                    },
                                ],
                            }
                            for index, metric in enumerate(metrics)
                        ],
                    ],
                },
            ],
        )

        figure.update_xaxes(showgrid=True, domain=cls.CHART_X_DOMAIN)
        figure.update_yaxes(showgrid=True, rangemode="tozero")
        figure.update_layout(cls._chart_axis_updates(initial_chart))

        return figure

    @classmethod
    def show(
        cls,
        dashboard: RepositoryDashboardViewModel,
    ) -> None:
        """Создаёт и отображает интерактивный дашборд репозитория."""
        figure = cls.build_figure(dashboard)
        figure.show(config={"responsive": True})

    @classmethod
    def save_html(
        cls,
        dashboard: RepositoryDashboardViewModel,
        filepath: str,
    ) -> None:
        """Cохраняет интерактивный дашборд репозитория в виде HTML-файла."""
        figure = cls.build_figure(dashboard)
        figure.write_html(
            filepath,
            config={"responsive": True},
            default_width="100%",
            default_height="100vh",
        )

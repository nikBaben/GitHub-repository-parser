import plotly.graph_objects as go

from parser.presentation.chart.line_chart import HistoryChartModel


class PlotlyHistoryPlotter:
    """Построитель исторических графиков на основе Plotly."""
    @staticmethod
    def build_figure(
        chart: HistoryChartModel,
        chart_kind: str = "bar",  # "bar" | "line"
    ) -> go.Figure:
        """Создаёт Plotly-фигуру исторического графика."""
        x_values = [point.ts for point in chart.points]
        y_values = [point.value for point in chart.points]

        figure = go.Figure()

        if not chart.points:
            figure.update_layout(
                title=chart.title,
                xaxis_title=chart.x_title,
                yaxis_title=chart.y_title,
                template="plotly_white",
            )
            return figure

        if chart_kind == "bar":
            figure.add_trace(
                go.Bar(
                    x=x_values,
                    y=y_values,
                    name=chart.y_title,
                    hovertemplate=(
                        "Period start: %{x|%Y-%m-%d}<br>"
                        "Count: %{y}<extra></extra>"
                    ),
                )
            )
        elif chart_kind == "line":
            figure.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines+markers",
                    name=chart.y_title,
                    hovertemplate=(
                        "Period start: %{x|%Y-%m-%d}<br>"
                        "Count: %{y}<extra></extra>"
                    ),
                )
            )
        else:
            raise ValueError("chart_kind must be 'bar' or 'line'")

        figure.update_layout(
            title={
                "text": chart.title,
                "x": 0.5,
            },
            xaxis_title=chart.x_title,
            yaxis_title=chart.y_title,
            template="plotly_white",
            hovermode="x unified",
            margin={"l": 50, "r": 30, "t": 80, "b": 60},
        )

        figure.update_xaxes(showgrid=True)
        figure.update_yaxes(showgrid=True, rangemode="tozero")

        return figure

    @staticmethod
    def show(chart: HistoryChartModel, chart_kind: str = "bar") -> None:
        """Создаёт и отображает исторический график."""
        figure = PlotlyHistoryPlotter.build_figure(chart=chart, chart_kind=chart_kind)
        figure.show()

    @staticmethod
    def save_html(
        chart: HistoryChartModel,
        filepath: str,
        chart_kind: str = "bar",
    ) -> None:
        """Cохраняет исторический график в виде HTML-файла."""
        figure = PlotlyHistoryPlotter.build_figure(chart=chart, chart_kind=chart_kind)
        figure.write_html(filepath)
import asyncio

from infrastructure.github.config import settings
from infrastructure.github.clients.client import GitHubClient
from infrastructure.di.container import AppContainer
from application.queries.queries import GetHistoryQuery
from presentation.mappers import RepositoryDashboardMapper

async def main() -> None:
    async with GitHubClient(settings.TOKEN) as github_client:
        container = AppContainer(github_client)

        get_history_use_case = container.get_history_use_case()
        analytics_use_case = container.analytics_use_case()
        dashboard_render = container.repository_dashboard_renderer()

        query = GetHistoryQuery(
            url=settings.GITHUB_URL,
            days=settings.DAYS
        )

        history = await get_history_use_case.execute(query)
        analytics = analytics_use_case.execute(history)
        print("=== HISTORY ===")
        print(history.model_dump(mode="json"))

        print("\n=== ANALYTICS ===")
        print(analytics.model_dump(mode="json"))

        dashboard = RepositoryDashboardMapper.to_view_model(
            history=history,
            analytics=analytics,
            bucket="week",
        )

        dashboard_render.show(dashboard)
        dashboard_render.save_html(
            dashboard=dashboard,
            filepath="repository_analytics_dashboard.html",
        )


if __name__ == "__main__":
    asyncio.run(main())
